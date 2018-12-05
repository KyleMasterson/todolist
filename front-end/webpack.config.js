const path = require("path")
const webpack = require("webpack")
const HtmlWebpackPlugin = require("html-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");
const HtmlBeautifyPlugin = require("html-beautify-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const CleanWebpackPlugin = require("clean-webpack-plugin");

const mode = process.env.NODE_ENV;
if (mode === undefined) {
    throw Error("NODE_ENV is not set!");
}

const config = {
    mode: mode,
    entry: "./src/main.js",
    output: {
        path: path.resolve(__dirname, "dist"),
        publicPath: "/dist/",
        filename: "bundle.js"
    },
    plugins: [
        new CleanWebpackPlugin(["./dist"]),
        new HtmlWebpackPlugin({ template: "src/index.html" }),
        new VueLoaderPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: "vue-loader",
            },
            {
                test: /\.(png|jpg|gif|svg|ico)$/,
                loader: "file-loader",
                options: {
                    name: "[name].[ext]"
                }
            },
            {
                test: /\.css$/, 
                use: [
                    "vue-style-loader", 
                    "css-loader"
                ]
            }
        ]
    },
    resolve: {
        extensions: [".ts", ".js", ".vue", ".json"],
        alias: {
            "vue$": "vue/dist/vue.esm.js"
        }
    },
    performance: {
        hints: false
    },
};

module.exports = (env, argv) => {
    if (mode === "development") {
        config.devtool = "eval-source-map";
    }
    else if (mode === "production") {
        config.devtool = "source-map";
    }

    return config;
};