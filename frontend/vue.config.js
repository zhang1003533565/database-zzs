module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // Django 后端地址
        changeOrigin: true,
      }
    }
  }
}
