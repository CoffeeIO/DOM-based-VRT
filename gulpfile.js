// Ordered set of TypeScript files to load. -----------------------------------
var source = [
    'src/a.pre.js',
    'src/domvrt.differ.js',
    'src/domvrt.extractor.js',
    'src/domvrt.utils.js',
    'src/z.post.js',
];
var librarySource = [
    'src/vendor/FileSaver.js',
    'src/vendor/html2canvas.min.js',
    'src/vendor/dom-to-image.min.js',
];
// ----------------------------------------------------------------------------

// Initialize gulp variables.
var gulp = require("gulp");
var concat = require('gulp-concat');
var sass = require('gulp-sass');
var watch = require('gulp-watch');
var babel = require("gulp-babel");
var ts = require('gulp-typescript');
var minify = require('gulp-minify');

gulp.task('ts', function () {
    return gulp.src(source)
        .pipe(concat('domvrt.js'))
        // .pipe(babel())
        .pipe(gulp.dest("ChromeExtension"));
});

gulp.task('vendor', function () {
    return gulp.src(librarySource)
        .pipe(concat('domvrt.vendor.js'))
        .pipe(gulp.dest("ChromeExtension"));
});

gulp.task('merge', function () {
    return gulp.src([
            'ChromeExtension/domvrt.vendor.js',
            'ChromeExtension/domvrt.js',
        ])
        .pipe(concat('domvrt.js'))
        .pipe(gulp.dest("ChromeExtension"));
});

var tasks = [
    // 'vendor', // Bundle vendor files
    'ts',         // Compile Typescript files
    // 'merge',   // Merge vendor files with typescript files
];

gulp.task('compile', gulp.series(tasks))
gulp.task('watch-src', function() {
    return watch('src/**/*', gulp.series(tasks));
});
gulp.task('watch', gulp.series('compile', 'watch-src'));
gulp.task("default", gulp.series('compile'));