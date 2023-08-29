const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave:false,
  devServer:{
    allowedHosts:"all",
    historyApiFallback:true
  },
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
        Object.assign(definitions[0]['process.env'], {
          NODE_HOST: '"http://127.0.0.1:8888"',
        });
        return definitions;
    });
  }
  // devServer: {
  //   host: '124.126.102.124', // 项目运行的ip
  //   port: 8080, // 项目运行的端口号
  // }
})
