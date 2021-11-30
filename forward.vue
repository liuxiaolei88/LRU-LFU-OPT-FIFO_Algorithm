
<template>
  <el-menu
    :default-active="activeIndex"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
  >
    <el-menu-item index="1">操作系统课设</el-menu-item>
    <el-menu-item index="2" disabled>页面置换算法模拟</el-menu-item>
    <el-menu-item index="3" disabled>Author@ XiaoLei Liu</el-menu-item>
  </el-menu>
  <div class="line"></div>

  <div class="con">
    <div class="demo-input-suffix">
      <span class="demo-input-label"
        >请输入物理块号，两个块号以空格分开，支持0~9的输入</span
      >

      <el-row :gutter="20">
        <el-input v-model="input1" placeholder="请输入" />
      </el-row>
      <span class="demo-input-label">请输入内存大小</span>
      <el-row :gutter="20">
        <el-input v-model="input2" placeholder="请输入">
          <template #suffix>
            <el-icon class="el-input__icon"><calendar /></el-icon>
          </template>
        </el-input>
      </el-row>
      <span class="demo-input-label">请选择算法：1:OPT 2:FIFO 3:LRU 4:LFU </span>
      <el-row :gutter="20">
        <el-input v-model="input3" placeholder="请输入">
          <template #suffix>
            <el-icon class="el-input__icon"><calendar /></el-icon>
          </template>
        </el-input>
      </el-row>
      <el-row :gutter="20"> </el-row>
      <el-button class="button" @click="hi" type="primary" :icon="Search">Run</el-button>
    </div>

    

    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>结果输出</span>
          
        </div>
      </template>
      <div v-for="o in res.value" :key="o" class="text item">
        {{ "" + o }}
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import { Calendar, Search } from "@element-plus/icons";

export default {
  setup() {
    const res = reactive({ value: [-1, -1, -1]});
    let hi = async function () {
      let data = await fetch("http://10.102.175.182:5000/hi", {
        method: "post",
        body: JSON.stringify({
          x: input1.value,
          y: input2.value,
          z: input3.value,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      let str = await data.text();
      let resArr = str
        .substring(1, str.length - 1)
        .split("][")
        .map((item) => {
          return item.split(", ").map(Number);
        });
      res.value = resArr;
      for (let i of res.value) console.log(i);
    };

    const input1 = ref("");
    const input2 = ref("");
    const input3 = ref("");
    const activeIndex = ref("1");
    const activeIndex2 = ref("1");
    const handleSelect = (key, keyPath) => {
      console.log(key, keyPath);
    };
    return {
      input1,
      input2,
      input3,
      res,
      activeIndex,
      activeIndex2,
      handleSelect,
      Calendar,
      Search,
      hi,
    };
  },
};
</script>

<style>

.demo-input-label {
  display: inline-block;
  width: 530px;
  margin-bottom: 10px;
  margin-top: 15px;
}

.demo-input-suffix {
  margin-bottom: 16px;
  width: 30%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 480px;
  margin-left: 200px;
  margin-top: 15px;
}
.con {
  width: 90vw;
  margin-left: 5vw;
  display: flex;
  margin-top: 30px;
}
.button{
  margin-top: 30px;
}
</style>
