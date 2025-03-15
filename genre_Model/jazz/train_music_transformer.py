import tensorflow as tf
from tensorflow.keras.layers import Embedding, Dense, LayerNormalization, Dropout
from tensorflow.keras.models import Model
import numpy as np


class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, sequence_length, d_model):
        super(PositionalEncoding, self).__init__()
        self.sequence_length = sequence_length
        self.d_model = d_model

    def get_angles(self, pos, i):
        angle_rates = 1 / np.power(10000, (2 * (i // 2)) / np.float32(self.d_model))
        return pos * angle_rates

    def call(self, inputs):
        batch_size = tf.shape(inputs)[0]
        positions = np.arange(self.sequence_length)[:, np.newaxis]
        indices = np.arange(self.d_model)[np.newaxis, :]
        angle_rads = self.get_angles(positions, indices)

        angle_rads[:, 0::2] = np.sin(angle_rads[:, 0::2])
        angle_rads[:, 1::2] = np.cos(angle_rads[:, 1::2])

        pos_encoding = tf.cast(angle_rads[np.newaxis, ...], dtype=tf.float32)
        return inputs + pos_encoding[:, :tf.shape(inputs)[1], :]  # ✅ 크기 맞추기


class MultiHeadAttention(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads):
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0
        self.num_heads = num_heads
        self.depth = d_model // num_heads

        self.wq = Dense(d_model)
        self.wk = Dense(d_model)
        self.wv = Dense(d_model)

        self.dense = Dense(d_model)

    def split_heads(self, x, batch_size):
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])

    def call(self, v, k, q, mask=None):  # ✅ mask=None 기본값 설정
        batch_size = tf.shape(q)[0]

        q = self.split_heads(self.wq(q), batch_size)
        k = self.split_heads(self.wk(k), batch_size)
        v = self.split_heads(self.wv(v), batch_size)

        scores = tf.matmul(q, k, transpose_b=True) / tf.math.sqrt(tf.cast(self.depth, tf.float32))

        if mask is not None:
            scores += (mask * -1e9)

        attention_weights = tf.nn.softmax(scores, axis=-1)
        output = tf.matmul(attention_weights, v)
        output = tf.transpose(output, perm=[0, 2, 1, 3])
        output = tf.reshape(output, (batch_size, -1, self.num_heads * self.depth))

        return self.dense(output)


class FeedForwardNetwork(tf.keras.layers.Layer):
    def __init__(self, d_model, dff):
        super(FeedForwardNetwork, self).__init__()
        self.dense1 = Dense(dff, activation='relu')
        self.dense2 = Dense(d_model)

    def call(self, inputs):
        return self.dense2(self.dense1(inputs))


class TransformerBlock(tf.keras.layers.Layer):
    def __init__(self, d_model, num_heads, dff, dropout_rate=0.1):
        super(TransformerBlock, self).__init__()
        self.mha = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForwardNetwork(d_model, dff)

        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(dropout_rate)
        self.dropout2 = Dropout(dropout_rate)

    def call(self, inputs, mask=None):
        attn_output = self.mha(inputs, inputs, inputs, mask)
        attn_output = self.dropout1(attn_output)
        out1 = self.layernorm1(inputs + attn_output)

        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output)
        out2 = self.layernorm2(out1 + ffn_output)

        return out2


class MusicTransformer(Model):
    def __init__(self, sequence_length, d_model, num_heads, dff, num_layers, vocab_size, dropout_rate=0.1):
        super(MusicTransformer, self).__init__()
        self.embedding = Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(sequence_length, d_model)
        self.transformer_blocks = [TransformerBlock(d_model, num_heads, dff, dropout_rate) for _ in range(num_layers)]
        self.dropout = Dropout(dropout_rate)
        self.final_layer = Dense(vocab_size, activation='softmax')

    def call(self, inputs, mask=None):
        x = self.embedding(inputs)
        x = self.pos_encoding(x)
        x = self.dropout(x)

        for block in self.transformer_blocks:
            x = block(x)

        return self.final_layer(x)


# ✅ 모델 생성
batch_size = 32  # or 다른 적절한 값
sequence_length = 10
d_model = 128
num_heads = 8
dff = 512
num_layers = 4
vocab_size = 128  # MIDI 범위 (0~127)

model = MusicTransformer(sequence_length, d_model, num_heads, dff, num_layers, vocab_size)

# ✅ 모델 컴파일
model.compile(
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # ✅ 수정!
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
    metrics=['accuracy']
)


# ✅ 모델 빌드 (batch_size 지정)
model.build(input_shape=(batch_size, sequence_length))

# ✅ 가짜 입력 데이터를 한 번 통과시켜 강제 빌드
dummy_input = np.random.randint(0, vocab_size, size=(1, sequence_length))
_ = model(dummy_input)

# ✅ 모델 구조 출력
model.summary()