const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './src/background.ts',
  devtool: 'inline-source-map',
  optimization: {
    minimize: false
  },
  module: {
    rules: [
      {
        test: /\.ts?$/,
        use: 'ts-loader',
      }
    ]
  },
  resolve: {
    extensions: ['.ts', '.js']
  },
  output: {
    filename: 'background.js',
    path: path.resolve(__dirname, 'build', 'unpacked'),
    publicPath: './build/unpacked',
  },
  plugins: [
    new CopyWebpackPlugin([{
      from: "./src/manifest.json",
      to: "./manifest.json"
    }])
  ]
};
