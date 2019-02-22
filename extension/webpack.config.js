const fs = require('fs');
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
      from: './src/manifest.json',
      to: './manifest.json',
      transform: (content, path) => {
        const data = JSON.parse(content);
        const buildFile = './local/build.json';
        console.log(buildFile);
        const buildInfo = fs.existsSync(buildFile) ?
          JSON.parse(fs.readFileSync(buildFile, 'utf8'))
          : {version: -1};
        buildInfo.version += 1;
        data['version'] += `.${buildInfo.version}`;
        fs.writeFileSync(buildFile, JSON.stringify(buildInfo, null, 2));
        return JSON.stringify(data, null, 2);
      }
    }])
  ]
};
