const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: 'development',
    entry: './src/renderer/main.js', // Ensure this points to your main renderer entry file
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.svelte$/,
                use: {
                    loader: 'svelte-loader',
                    options: {
                        emitCss: true,
                        hotReload: true
                    }
                }
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    },
    resolve: {
        extensions: ['.mjs', '.js', '.svelte'],
        fallback: {
            "fs": false, // Electron apps don't need 'fs' in the renderer process
            "path": require.resolve("path-browserify") // Polyfill for 'path'
        }
    },
    plugins: [
        new HtmlWebpackPlugin({
            template: './public/index.html' // Ensure your HTML template exists
        })
    ],
    devServer: {
        static: {
            directory: path.join(__dirname, 'dist'),
        },
        compress: true,
        port: 8080
    }
};
