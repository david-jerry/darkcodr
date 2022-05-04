const postcssPresetEnv = require("postcss-preset-env");

const postcssImport = require('postcss-import');
const postcssVars = require("postcss-simple-vars");
const postcssNested = require('postcss-nested');
const postcssMinify = require("postcss-minify");
const postcssPrefixer = require("autoprefixer");


module.exports = {
  plugins: [
    postcssPresetEnv(),
    postcssImport(),
    postcssVars(),
    postcssNested(),
    postcssMinify(),
    postcssPrefixer(),
  ],
};
