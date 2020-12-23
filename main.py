import csv
import codecs
import pandas as pd
from pykakasi import kakasi

#kakasi instance
kakasi = kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
conv = kakasi.getConverter()

#inport
domains = pd.read_table(
    filepath_or_buffer='./library/tld-list-basic.csv', header=None)
df = pd.read_table(filepath_or_buffer="./library/s_kotowaza.tsv",
                   encoding="ms932", header=None)

#単語のみ取り出し
df = df.drop(columns=df.columns[[1, 2]])

#ローマ字変換
result = []
for word in df[0]:
    result.append(conv.do(word))
df[1] = result
#正規表現エラー出るので仕方なく
df[1] = df[1].str.replace(".", "")
df[1] = df[1].str.replace("'", "")

#ドメイン一致判定
for word in domains[0]:
    df[word] = df[1].str.endswith(word)
df = df[df != False].dropna(how='all', axis='columns')

#ドメイン生成、detaframe整形
df_result = df.iloc[0:0]
for index in df.columns[2:]:
    df_ele = df[df[index] == 1.0].copy()
    df_ele[1] = df_ele[1].str.strip(index) + '.' + index
    df_result = pd.concat([df_result, df_ele], axis=0)
    df_result = df_result[[0, 1]]
print(df_result)

df_result.to_csv("kusodomain_kotowaza.csv", index=False)
