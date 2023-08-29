<template>
  <div class="chat">
    <div class="left">
      <div class="left_top" >
        <el-button class="add" icon="el-icon-plus" @click="newChat">新聊天</el-button>
      </div>
      <div class="left_center" >
        <el-button round v-for="(session,index) in sessions" :key="index" class="session" :class="{active:session.active}" @click="changeSession(index)">
          <i class="el-icon-chat-dot-round">{{session.name}}</i>
        </el-button>
      </div>
      <div class="left_buttom">
          <el-button class="clear" icon = "el-icon-delete" @click="clearSessions">
            清空会话
          </el-button>
      </div>
    </div>
    <div class="right">
      <div v-if="sessions.length !== 0"  class="chatbox" ref="sessions">
        <div v-for="(session,index) in sessions" class="sessions" :key="index" v-show="session.active">
          <div class="right_top">
            <div v-if="session.messages.length === 0" class="messages" ref="session">
              <div class="title">
                <h1>myChat</h1>
              </div>
              <div class="examples">
                <div class="examples1">
                  <div class="example">
                    <div class="example-title">
                      <i class="el-icon-sunny">示例</i>
                    </div>
                    <button v-for="(info,index) in infos" :key="index" class="example-list" @click="clickExample(index)">
                      {{ info }}
                    </button>
                  </div>
                  <div class="example">
                    <div class="example-title">
                      <i class="el-icon-sunny">示例</i>
                    </div>
                    <button v-for="(info,index) in infos2" :key="index" class="example-list" @click="clickExample2(index)">
                      {{ info }}
                    </button>
                  </div>
                  <div class="limitations">
                    <div class="example-title">
                      <i class="el-icon-warning-outline">限制</i>
                    </div>
                    <button v-for="(limitation,index) in limitations" :key="index" class="example-list">
                      {{ limitation }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="messages" ref="messages">
              <div v-for="(message, index) in session.messages" :key="index" class="message" :class="{'my-message': message.sender === 'me', 'other-message': message.sender === 'other'}">
                <div v-if="message.sender === 'me'" class="message-sender">
                  <img src="../assets/imgs/user.png">
                </div>
                <div v-else-if="message.sender === 'other'" class="message-sender">
                  <img src="../assets/imgs/system.jpeg">
                </div> 
                <div class="message-text">
                  <pre>{{ message.text }}</pre>
                </div>
              </div>
            </div>
          </div>
          <div class="right_buttom">
            <div v-show="!state">
              <el-button @click="stopContent">
                stop
              </el-button>
            </div>
            <div class="text">
              <el-input class="input" v-model="session.newMessage" placeholder="please input" @keyup.enter.native="sendMessage()">
              </el-input>
              <el-button style="border:none" class="send" icon = "el-icon-s-promotion" @click="sendMessage()">
                    发送
              </el-button>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="sessions.length === 0" class="chatbox" ref="sessions">
        <div class="right_top">
          <div class="title">
            <h1>医疗知识问答系统</h1>
          </div>
          <div class="examples">
            <div class="examples1">
              <div class="example">
                <div class="example-title">
                  <i class="el-icon-sunny">示例</i>
                </div>
                <button v-for="(info,index) in infos" :key="index" class="example-list" @click="clickNewExample(index)">
                  {{ info }}
                </button>
              </div>
              <div class="example">
                <div class="example-title">
                  <i class="el-icon-sunny">示例</i>
                </div>
                <button v-for="(info,index) in infos2" :key="index" class="example-list" @click="clickNewExample2(index)">
                  {{ info }}
                </button>
              </div>
              <div class="limitations">
                <div class="example-title">
                  <i class="el-icon-warning-outline">限制</i>
                </div>
                <button v-for="(limitation,index) in limitations" :key="index" class="example-list">
                  {{ limitation }}
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="right_buttom">
          <div class="text">
            <el-input class="input" v-model="newMessage" placeholder="please input" @keyup.enter.native="sendNewMessage()">
            </el-input>
            <el-button style="border:none" class="send" :class="{active:state}" icon = "el-icon-s-promotion" @click="sendNewMessage()">
              发送
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { HttpManager } from "@/api";
export default{
  data() {
    return {
      timer:'',
      state:true,
      stop:false,
      selectedIndex:-1,
      infos:["高血压的症状","白血病的病因","感冒不能吃什么","高血压推荐吃什么食物","白血病的治愈率"],
      infos2:["感冒用什么药","藿香正气丸的功效","哮喘的常识","支气管肺炎要做什么检查","感冒的治疗时间"],
      limitations:["我只能回答与医疗有关的问题","我的知识库中没有收录的疾病也无法查询","我只能回答与示例类似的问题"],
      sessions:[],
      message:[],
      newMessage:"",
      textCount:0
    };
  },
  methods: {
    changeSession(index) {
      this.sessions.forEach((session, i) => {
        session.active = i === index;
      });
      this.selectedIndex = index
    },
    newChat() {
      this.state=true
      this.sessions.forEach((session, i) => {
        session.active = false
      })
      this.selectedIndex += 1
      this.sessions.push({
        name:"NewChat",
        messages:[],
        newMessage:"",
        active:true
      })
      console.log(this.selectedIndex);
    },
    async sendMessage() {
      if (this.state) {
        if (this.sessions[this.selectedIndex].newMessage) {
          if(this.stop == true) {
            this.stop = false;
          }
          if(this.sessions[this.selectedIndex].messages.length === 0) {
            this.sessions[this.selectedIndex].name = this.sessions[this.selectedIndex].newMessage
          }
          this.sessions[this.selectedIndex].messages.push({ sender: 'me', text: this.sessions[this.selectedIndex].newMessage });
          let result = (await HttpManager.query(this.sessions[this.selectedIndex].newMessage)) 
          let text = ""
          result.data.forEach(element => {
            text += element
          });
          console.log(text);
          console.log(this.stop);
          this.sessions[this.selectedIndex].messages.push({sender:"other",text:""})
          let len = this.sessions[this.selectedIndex].messages.length
          this.getChatContent(this.selectedIndex,text,len-1)
          this.sessions[this.selectedIndex].newMessage = ""
        }
        this.textCount = 0
      }
    },
    // 延时函数
    sleep(delaytime = 10000) {
      return new Promise(resolve => setTimeout(resolve, delaytime));
    },
    // 同步遍历，自定义延时时间
    async delayDo(
      iterList,
      callback = data => console.log(`数据：${data}`),
      delaytimeList
    ) {
      let len = iterList.length;
      for (let i = 0; i < len; i++) {
        callback(iterList[i], i);
        await this.sleep(delaytimeList[i]);
      }
    },
    stopContent() {
      this.stop = true;
      this.state = true;
    },
    getChatContent(selectIdx,text, index) {
      this.timer = setInterval(() => {
        this.textCount+=1;
        if(!this.stop) {
          if (this.textCount == text.length + 1) {
            this.textCount = 0;
            this.sessions[selectIdx].messages.splice(index, 1, { sender:"other", text:text});
            this.state = true;
            clearInterval(this.timer);
            return;
          }
          // 取字符串子串
          let nowStr = text.substring(0, this.textCount);
          this.state = false;
          this.sessions[selectIdx].messages.splice(index, 1, { sender:"other", text:nowStr});
        }
        if(this.stop) {
          clearInterval(this.timer);
          this.state = true;
          return;
        }
      }, 50);
    },
    async sendNewMessage() {
      if(this.state) {
        if(this.newMessage) {
          this.selectedIndex += 1
          if(!this.stop == true) {
            this.stop = false;
          }
          this.sessions.push({
            name:this.newMessage,
            messages: [{sender:"me",text:this.newMessage}],
            newMessage:"",
            active:true
          })
          let result = (await HttpManager.query(this.newMessage)) 
          let text = ""
          result.data.forEach(element => {
            text += element
          });
          this.sessions[this.selectedIndex].messages.push({sender:"other",text:""})
          let len = this.sessions[this.selectedIndex].messages.length
          this.getChatContent(this.selectedIndex,text,len-1)
          this.newMessage = ""
          this.textCount = 0
        }
      }
      
    },
    clickExample(index) {
      console.log(this.selectedIndex);
      this.sessions[this.selectedIndex].newMessage = this.infos[index]
    },
    clickExample2(index) {
      this.sessions[this.selectedIndex].newMessage = this.infos2[index]
    },
    clickNewExample(index) {
      this.newMessage = this.infos[index]
    },
    clickNewExample2(index) {
      this.newMessage = this.infos2[index]
    },
    clearSessions() {
      this.sessions = []
      this.selectedIndex = -1
    },
    clearMessages() {
      
    }
  }
};
</script>

<style scoped>
.chat {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
.left {
  width: 17%;
  height: 100%;
  background-color:rgb(32, 33, 35);
  display: flex;
  flex-direction: column;
}
.left_top {
  width: 100%;
  height: 5%;
  display: flex;
  justify-content: center;
}
.left_center {
  width: 100%;
  height: 55%;
  display: flex;
  flex-direction: column;
  justify-content: left;
}
.left_buttom {
  width: 100%;
  height: 40%;
}
.add:hover {
  background-color: rgb(32, 33, 35);
}
.add {
  width: 95%;
  height: 100%;
  display: flex;
  text-align: center;
  background-color: rgb(32, 33, 35);
  color:rgb(255,255,255);
}
.el-button.is-round {
  margin-left: 0px;
}
.session:hover {
  background-color: rgb(42, 43, 50);
}
.session.active {
  background-color: rgb(52, 53, 65);
}
.session{
  width: 98%;
  height: 10%;
  border:none;
  background-color: rgb(32, 33, 35);
  color:rgb(255,255,255);
}
.clear {
  width: 100%;
  background-color: rgb(32, 33, 35);
  border:none;
  color:rgb(255,255,255);
}
.clear:hover,.clear:focus {
  background-color: rgb(42, 43, 50);
}
 .right {
  width: 83%;
  height: 100%;
  display: block;
}
.right_top {
  width: 100%;
  height: 80%;
}
.right_buttom {
  width: 100%;
  height: 18%;
  justify-content: center;
  align-items: center;
}
.text {
  width: 60%;
  height: 40%;
  position: relative;
  margin: auto;
  justify-content: center;
  display: flex;
}
.sessions {
  width: 100%;
  height: 100%;
}
.input {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  /* align-items: center; */
}
.el-input__inner {
  height: 100px;
}
.el-button.send {
  padding:0px;
  height: 40px;
}
.chatbox {
  border: 1px solid #ccc;
  height: 100%;
  /* padding: 10px; */
  /* border-radius: 5px; */
}

.messages {
  height: 100%;
  overflow-y: scroll;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.message {
  background-color: #eee;
  padding: 5px;
  border-radius: 5px;
  margin-bottom: 5px;
  min-width: 99%;
  max-width: 100%;
  display: flex;
  text-align: left;
}

.my-message {
  /* float: right; */
  background-color: #fff;
  color:black;
}

.other-message {
  float: left;
}

.message-sender {
  font-weight: bold;
  width: 5%;
}
.message-text {
  width: 95%;
}
.title {
  width: 100%;
  height: 25%;
  align-items: center;
  display: flex;
  justify-content: center;
}
.examples {
  width: 100%;
  height: 75%;
  align-items: center;
  display: flex;
  justify-content: center;
}
.examples1 {
  width: 80%;
  height: 80%;
  display: flex;
}
.example {
  width: 33.3%;
  height: 100%;
  margin-left: 5px;
}
.limitations {
  width: 33.3%;
  height: 100%;
  margin-left: 5px;
}
.example-list {
  width: 100%;
  height: 15%;
  border: none;
  margin: 10px;
  background-color: rgb(247, 247, 248);
}
.example-list:hover {
  background-color: rgb(217, 217, 227);
}
pre {
  white-space: pre-wrap;
}
</style>
