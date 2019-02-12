# Auto_Attendance_Management
<!-- TOC -->
目次
==
- [概要](#概要)
- [背景](#背景)
- [プログラム概要](#プログラム概要)
  - [前準備](#前準備)
  - [ディレクトリ構造](#ディレクトリ構造)
  - [Auto_Attend.py](#Auto_Attend.py)
  - [SubmitForm](#SubmitForm)
  - [TemplateForm](#templateform)
  - [プログラム環境](#プログラム環境)
<!-- /TOC -->

# 概要
僕が所属している大学の研究室が担当している講義の出席管理のプログラムです  
このコマンドを打てば動きます  
講義日は例えば１２月４日なら1204、４月２３日なら0423な感じで
```
python Auto_Attend.py {講義日}
```

# 背景
研究室の教授の授業の出席は、講義で出題される課題を記入する欄と名前、学籍番号、質問の項目がある用紙が配られます。

その用紙には学籍番号を記入するワークシートがありました👇

<img src='./TemplateForm/student_number_form.jpg' width='500'>


講義を受けていた時はてっきり、このマークを読み込んで出席管理をしているんだな〜
と思っていたのですが、

いざ、研究室に配属されると、マークシートは使わず記入された学籍番号を学生が確認し、エクセルファイルに打ち込むじゃありませんか！！

大変ですね

その後、研究室の同期とこの話になった時に

 **「これを自動化できるプログラム作れるくない？」**

 **なので、作ってみました<br/>**
<br>
<br>

# プログラム概要
## 前準備
講義で提出された用紙をスキャナーとかを使ってjpgファイルとして保存する  
ファイル名は 1.jpg、2.jpg、3.jpg … とする  

## ディレクトリ構造
ディレクトリ構造はこちら

## Auto_Attend.py
これがこのプログラムの mainファイルです  
このファイルを実行します実行方法は別の項目で

## SubmitForm
&emsp;ここに用紙のjpgファイルを保存してください 
&emsp;遅刻ならLateArrival（これはいらない）、マークが未記入ならAnonymous（これもいらない）へファイルが移動します

## TemplateForm
&emsp;ここはプログラムで使用する３つのテンプレート画像があります。説明が面倒くさいので画像貼ります  
&emsp;（画像の説明は省力で）
<br>
<br>
<img src='./TemplateForm/00.png' width="200px">&emsp;&emsp;&emsp;
<img src='./TemplateForm/marked_point_img.png' width='100'>

最後の一枚は上で貼ったマークシートです
<br>
<br>

## プログラム環境

プログラム環境についても書いておきます（使用バージョン外の動作は確認していません）

## プログラムの流れ
ソースコードに沿って説明していると長くなってしまうので、ここではコードを載せずに簡単に説明します  
（暇だったらQiitaに載せるかも）  

1. 