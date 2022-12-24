module.exports = {
  css: {
    loaderOptions: {
      // передача настроек в sass-loader
      // @/ это псевдоним к каталогу src/ поэтому предполагается,
      // что у вас в проекте есть файл `src/variables.scss`
      // Примечание: эта опция называется "prependData" в sass-loader v8
      scss: {
        additionalData: `@import "~@/variables.scss";`
      },
    }
  },
  devServer: {
    proxy: 'http://backend:1337'
  }
}
