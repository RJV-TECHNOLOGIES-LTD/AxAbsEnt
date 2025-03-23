// web/webpack.config.js

const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");
const webpack = require("webpack");

module.exports = (env, argv) => {
  const isProduction = argv.mode === "production";

  return {
    entry: "./src/index.js",

    output: {
      path: path.resolve(__dirname, "dist"),
      filename: isProduction ? "[name].[contenthash].js" : "[name].js",
      publicPath: "/",
    },

    resolve: {
      extensions: [".js", ".jsx"],
      alias: {
        "@components": path.resolve(__dirname, "src/components/"),
        "@services": path.resolve(__dirname, "src/services/"),
        "@utils": path.resolve(__dirname, "src/utils/"),
        "@images": path.resolve(__dirname, "public/images/"),
      },
    },

    devtool: isProduction ? "source-map" : "eval-source-map",

    devServer: {
      static: path.join(__dirname, "public"),
      compress: true,
      hot: true,
      historyApiFallback: true,
      port: 3000,
      open: true,
      client: {
        overlay: true,
      },
      proxy: {
        "/api": "http://localhost:8000",
      },
    },

    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: ["babel-loader"],
        },
        {
          test: /\.css$/,
          use: ["style-loader", "css-loader"],
        },
        {
          test: /\.(png|svg|jpg|jpeg|gif|ico)$/i,
          type: "asset/resource",
          generator: {
            filename: "assets/[name][ext]",
          },
        },
        {
          test: /\.html$/,
          use: ["html-loader"],
        },
      ],
    },

    plugins: [
      new CleanWebpackPlugin(),

      new HtmlWebpackPlugin({
        template: "./public/index.html",
        favicon: "./public/favicon.ico",
        title: "AxAbsEnt – Cross-Absolute Simulator",
      }),

      new webpack.DefinePlugin({
        "process.env.NODE_ENV": JSON.stringify(argv.mode),
      }),

      ...(isProduction
        ? []
        : [new webpack.HotModuleReplacementPlugin()]),
    ],

    optimization: {
      splitChunks: {
        chunks: "all",
      },
      runtimeChunk: "single",
    },
  };
};
