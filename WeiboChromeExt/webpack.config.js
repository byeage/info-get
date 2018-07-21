const path = require('path')
const PATHS = {
  background: path.join(__dirname, 'src/background.js'),
  content: path.join(__dirname, 'src/content.js'),
  monkeyPack: path.join(__dirname, 'src/monkeyPack.js'),
  build: path.join(__dirname, 'dist')
}

module.exports = {
  entry: {
    background: PATHS.background,
    content: PATHS.content,
    monkeyPack: PATHS.monkeyPack
  },
  output: {
    path: PATHS.build,
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader', {
          loader: 'eslint-loader',
          options: {
            fix: true
          }
        }]
      },
      {
        test: /\.css$/,
        loader: 'style-loader'
      }, {
        test: /\.css$/,
        loader: 'css-loader',
        query: {
          modules: true,
          localIdentName: '[name]__[local]___[hash:base64:5]'
        }
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }
}
