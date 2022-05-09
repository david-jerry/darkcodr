const glob = require("glob");
const Path = require("path");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const WebpackAssetsManifest = require("webpack-assets-manifest");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const FaviconsWebpackPlugin = require("favicons-webpack-plugin");
const { InjectManifest } = require('workbox-webpack-plugin');
const ImageMinimizerPlugin = require("image-minimizer-webpack-plugin");

const getEntryObject = () => {
  const entries = {};
  glob.sync(Path.join(__dirname, "../src/application/*.js")).forEach((path) => {
    const name = Path.basename(path, ".js");
    entries[name] = path;
  });
  return entries;
};

module.exports = {
  entry: getEntryObject(),
  output: {
    path: Path.join(__dirname, "../../darkcodr/static"),
    filename: "js/[name].js",
    publicPath: "/static/",
  },
  optimization: {
    splitChunks: {
      chunks: "all",
    },

    runtimeChunk: "single",
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyWebpackPlugin({
      patterns: [
        { from: Path.resolve(__dirname, "../vendors"), to: "vendors" },
      ],
    }),
    new FaviconsWebpackPlugin({
      // Your source logo (required)
      logo: "./vendors/images/logo.png",
      // Prefix path for generated assets
      prefix: "assets/",
      devMode: "webapp", // optional can be 'webapp' or 'light' - 'light' by default
      // Favicons configuration options. Read more on: https://github.com/evilebottnawi/favicons#usage
      favicons: {
          appName: "Darkcodr Codes", // Your application's name. `string`
          icons: {
              favicons: true, // Create regular favicons. `boolean`
              android: true, // Create Android homescreen icon. `boolean` or `{ offset, background }`
              appleIcon: true, // Create Apple touch icons. `boolean` or `{ offset, background }`
              appleStartup: false, // Create Apple startup images. `boolean` or `{ offset, background }`
              coast: false, // Create Opera Coast icon. `boolean` or `{ offset, background }`
              firefox: true, // Create Firefox OS icons. `boolean` or `{ offset, background }`
              windows: true, // Create Windows 8 tile icons. `boolean` or `{ background }`
              yandex: true, // Create Yandex browser icon. `boolean` or `{ background }`
          },
        },
    }),
    new HtmlWebpackPlugin(),
    new InjectManifest({
        swSrc: './src/sw.js',
        swDest: '../../darkcodr/templates/sw.js',
        maximumFileSizeToCacheInBytes: 5000000,
    }),
    new WebpackAssetsManifest({
      entrypoints: true,
      output: "manifest.json",
      writeToDisk: true,
      publicPath: true,
    }),
  ],
  resolve: {
    alias: {
      "~": Path.resolve(__dirname, "../src"),
    },
  },
  module: {
    rules: [
      {
        test: /\.mjs$/,
        include: /node_modules/,
        type: "javascript/auto",
      },
      {
        test: /\.(jpg|jpeg|png|gif|svg|webp)$/,
        use: [{
            loader: ImageMinimizerPlugin.loader,
            options: {
                minimizer: {
                    implementation: ImageMinimizerPlugin.imageminMinify,
                    options: {
                        plugins: [
                            "imagemin-gifsicle",
                            "imagemin-mozjpeg",
                            "imagemin-pngquant",
                            "imagemin-svgo",
                        ],
                    },
                }
            }
        }]
      },
      {
        test: /\.(ico|jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2)(\?.*)?$/,
        use: {
          loader: "file-loader",
          options: {
            name: "[path][name].[ext]",
          },
        },
      },
    ],
  },
};
