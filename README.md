# dingtalkdaka
自动执行钉打卡</br>需要配合windows的计划任务执行</br>
要求：</br>
一、安卓手机（已打开USB调试模式）</br>
二、数据线</br>
三、python2.7环境</br>
四、OpenCV 3.4</br>
五、AirCV</br>
</br>
运行方法：</br>
python dingtalkdaka.py  </br>
</br>

里面的各种jpg图片需要根据自己的手机分辨率进行适配截图。目前还没有做到缩放识别</br>

运行过程可以看demo.mp4
</br></br>
更新记录：</br>
2018-02-05</br>
新增节假日和换休日判断，根据specday.txt。</br>
specday.txt分为两个字段，加号表示当天要打卡，减号表示当天不要打卡。</br>
