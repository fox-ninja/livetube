# livetube
配信で作ったものを上げていきたいと思います。

2015/08/31<br>
livetube-tweetを追加しました。

2015/09/11<br>
livetube-tweetを更新しました。

ADVENTクソアプリ用テキスト<br>
本体：livetube-tweet.py

livetube（配信サイト）の配信情報が入ったjsonファイル（https://livetube.cc/index.live.json）を取得し、設定した名前とマッチングしたらTwitterにサムネ付きで配信告知する。<br>

私はこのサイトでたまに配信をしている。<br>
livetubeにはtwitter連携機能は無く、twitterにいちいち配信告知するのが面倒だったので、自動でツイートするものを作った。（cronで５分毎にlivetube-tweet.pyを動かしている）<br>
本当はPythonのwebフレームワークかnode electronなどを使って作り直し、一般人でも扱えるようにするつもりであったが、作らないままこの時を迎えてしまった。すまぬ(´；ω；｀)

クソなところ：
１．プログラミング初心者故、コードがクソ
２．一般人が扱いづらい
３．その他いろいろ
