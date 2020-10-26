# 実行
* make
    pukiwikiに書き出す

* make today
    今日のファイルを作成

* make upload
    添付していないファイルを送信
    送信前にリサイズを行う

* make resize
    resized.txtに記録されてないファイルをリサイズ

# util.py

sample
```python

text = get_text()
text.write("AAA")
response = text.set_text()
print(response)
```

# 書き方

画像(良い感じにリサイズ)
![img](./images/hoge.png)

リサイズ
![img:80%](./images/crx50ep_best_z23.png)

リンク
[github](https://github.com/kuangliu/pytorch-cifar)

// kkwiki begin

... ここに記事が挿入される

// kkwiki end
