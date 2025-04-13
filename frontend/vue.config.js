module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8006',  // Django 后端地址
        changeOrigin: true,
      }
    }
  }
}
