<template>
  <video id="videoElement"  autoplay muted style="background-color:#fff;height:600px;width:100%;"></video>
</template>

<script lang="ts">
import flvjs from 'flv.js'
import axios from "axios";

export default {
  name: 'flvjs',
  props: {
    src: {
      type: String,
      //default: 'http://127.0.0.1:8082/live?port=1935&app=live&stream=home'
        default: 'https://sf1-hscdn-tos.pstatp.com/obj/media-fe/xgplayer_doc_video/flv/xgplayer-demo-720p.flv'
    }
  },
  data () {
    return {
    }
  },
  mounted () {
    // axios({
    //   method: 'post',
    //   url: `http://127.0.0.1:8000/display/emo_stream/`,
    // })
    let flvSrc = this.src
    console.log('flvSrc:', flvSrc)
    if (flvjs.isSupported()) {
      var videoElement = document.getElementById('videoElement')
      var flvPlayer = flvjs.createPlayer({
        type: 'flv',
        // url: 'http://yunxianchang.live.ujne7.com/vod-system-bj/TLaf2cc9d469939803949187b46da16c45.flv'
        url: flvSrc
      })
      flvPlayer.attachMediaElement(videoElement)
      flvPlayer.load()
      flvPlayer.play()
    }
  },

  // onUnmounted() {
  //   axios({
  //     method: 'post',
  //     url: `http://127.0.0.1:8000/display/close_emotion_stream/`,
  //   })
  // }
}
</script>

<style lang="less" scoped>

</style>
