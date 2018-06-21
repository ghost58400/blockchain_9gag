<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
    <!-- Bootstrap CSS File  -->
    <link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.css"/>
    <link href="/css/main.css?1" rel="stylesheet">
<style>
summary {
    display: block;
}

audio,
canvas,
video {
    display: inline-block;
}

audio:not([controls]) {
    display: none;
    height: 0;
}

[hidden] {
    display: none;
}

html {
    font-family:Helvetica Neue,Arial,Helvetica,Geneva,sans-serif; 
    -ms-text-size-adjust: 100%; 
    -webkit-text-size-adjust: 100%; 
}

body {
    margin: 0;
	background-color:#EFEEEA;
	font-size:13px;
}

a:focus {
    outline: thin dotted;
}

a:active,
a:hover {
    outline: 0;
}

h1 {
    font-size: 2em;
    margin: 0.67em 0;
}

abbr[title] {
    border-bottom: 1px dotted;
}

b,
strong {
    font-weight: bold;
}

dfn {
    font-style: italic;
}

hr {
    -moz-box-sizing: content-box;
    box-sizing: content-box;
    height: 0;
}

mark {
    background: #ff0;
    color: #000;
}

code,
kbd,
pre,
samp {
    font-family: monospace, serif;
    font-size: 1em;
}

pre {
    white-space: pre-wrap;
}

q {
    quotes: "\201C" "\201D" "\2018" "\2019";
}

small {
    font-size: 80%;
}

sub,
sup {
    font-size: 75%;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
}

sup {
    top: -0.5em;
}

sub {
    bottom: -0.25em;
}

img {
    border: 0;
}

svg:not(:root) {
    overflow: hidden;
}

figure {
    margin: 0;
}

fieldset {
    border: 1px solid #c0c0c0;
    margin: 0 2px;
    padding: 0.35em 0.625em 0.75em;
}

legend {
    border: 0; /* 1 */
    padding: 0; /* 2 */
}

button,
input,
select,
textarea {
    font-family: inherit; 
    font-size: 100%; 
    margin: 0; 
}

button,
input {
    line-height: normal;
}

button,
select {
    text-transform: none;
}

button,
html input[type="button"], 
input[type="reset"],
input[type="submit"] {
    -webkit-appearance: button; 
    cursor: pointer; 
}

button[disabled],
html input[disabled] {
    cursor: default;
}

input[type="checkbox"],
input[type="radio"] {
    box-sizing: border-box; 
    padding: 0; 
}

input[type="search"] {
    -webkit-appearance: textfield; 
    -moz-box-sizing: content-box;
    -webkit-box-sizing: content-box; 
    box-sizing: content-box;
}

input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-decoration {
    -webkit-appearance: none;
}

button::-moz-focus-inner,
input::-moz-focus-inner {
    border: 0;
    padding: 0;
}

textarea {
    overflow: auto; /* 1 */
    vertical-align: top; /* 2 */
}

table {
    border-collapse: collapse;
    border-spacing: 0;
}
.clear{
	clear:both;
}

/* ==========================================================================
   end normalize css
   ========================================================================== */
   
   
/* begin top nav bar */

#top-nav{
	background-color:#000;
	width:100%;
	position:fixed;
	top:0;
	right:0;
	left:0;
	z-index:2000;
}

.main-nav{
	height:65px;
	width:960px;
	margin:0 auto;
	position:relative;
}
.main-nav a{
	text-decoration:none;
}

.main-nav h1 {
	margin:0px;
	float:left;
	height: 65px;
	width: 112px;
}

.main-nav h1 a { 
	display: block;
	height: 65px;
	width: 110px;
	background: url(/images/quickmeme.png) center no-repeat;
	text-indent: -9999px;
	overflow: hidden;
}
.main-nav h1 a:hover { 
	background: url(/images/quickmemehover.png) center no-repeat #2b2b2b;	
}

.menu-items{
	float:left;
	margin-left: 5px;
}
.new{
	display:none!important;
}
.menu-items ul{
	overflow: hidden;
	list-style-type: none;
	margin:0px;
	padding:0px;
}

.menu-items ul li{
	float:left;
}

.menu-items ul li a{
	display: block;
	color: #fff;
	line-height: 65px;
	height: 65px;
	padding: 0 15px;
}

.menu-items ul li a.current{
	color:#FFBF00;
}
.menu-items ul li a.current:hover{
	color:#FFBF00;
}
.menu-items ul li a:hover{
	color:#FFBF00;
	background-color: #333;
}

.user-functions{
	float:left;
	margin-top: 13px;
	margin-left:20px;
}
.user-functions a{
color: #fff;
border-top: #555 1px solid;
background-color: #383838;
padding: 10px 15px;
float: left;
border-radius: 3px;
-webkit-border-radius: 3px;
-moz-border-radius: 3px;
}
a.make-meme{
	background: url(/images/create.png) 10px center no-repeat #383838;
}
a.make-meme:hover{
	background: url(/images/createdark.png) 10px center no-repeat #333;
	color:#FFBF00;
	border-top: #333 1px solid;
}
.make-meme span{
	padding-left:20px;
	display:block;
}
a.upload-meme{
	background: url(/images/upload.png) 10px center no-repeat #383838;
}
a.upload-meme:hover{
	background: url(/images/uploaddark.png) 10px center no-repeat #333;
	color:#FFBF00;
	border-top: #333 1px solid;
}
.upload-meme span{
	padding-left:20px;
	display:block;
}
a.random-meme{
	background: url(/images/random.png) center no-repeat #383838;
	text-indent:-9999px;
	overflow:hidden;
	width:20px;
}
a.random-meme:hover{
	background: url(/images/randomdark.png) center no-repeat #333;
	color:#999;
	border-top: #333 1px solid;
}
.user-functions ul{
	overflow: hidden;
	list-style-type: none;
	margin: 0px;
	padding: 0px;
}

.user-functions ul li{
	float:left;
	margin-right:10px;
}

.nav-search{
	float:left;
	margin-top:17px;
}
.search-query{
	height: 20px;
	border-radius: 4px;
	background: #222;
	border: 1px solid #444;
	width: 105px;
	padding: 4px;
	color:#eee;
}
.user-login{
	float:right;
}
.user-login #fblogin img{
	width:30px;
	margin-top: 15px;
}
#shownsfw {
	display:none;
}
/* end top nav bar */

/*begin page content */
html {
  height:100%;
  background:black
}
body {
  min-height:100%;
  max-width:1100px;
  min-width:600px;
  margin:0 auto;
  background:white;
  color:black;
}
main {
  padding:1em;
}
a {
	color:#222;
	text-decoration:none;
}
a:hover {
	color:#8ca7dd;
}

#container{
	position:relative;
}
.page-content{
	width: 960px;
	margin: 102px auto 40px;
	overflow: hidden;
	position:relative;
}

.post-wrap{
	width:580px;
	float:left;
	position:relative;
}

#posts{
	margin: 20px 60px 0 0;
	width:520px;
	position:relative;
}
#loadmoreajaxloader {
	margin:0 auto;
	width:500px;
}
</style>
</head>
<body ng-app="App">
<!-- supplement sponsor -->
<a href="#" class="sponsor g"></a>
<a href="#" class="sponsor d"></a>
<!-- fin sponsor -->
<main>
<div id="top-nav">
	<div class="main-nav">
		<h1><a href="/">Memes.com : all your memes</a></h1>
	    <div class="menu-items">
			<ul>
			<li><a href="/news/">best</a></li><li><a href="/" class="current">what's hot</a></li>
		    
		</ul>
		</div><div class="user-functions">
		<ul>
        	<li><a href="/random" class="random-meme" title="randomize">random memes</a></li>
			<li><a href="/submit" class="upload-meme"><span>upload a funny</span></a></li>
            <li><a href="/caption" class="make-meme"><span>caption a meme</span></a></li>
		</ul>
	    </div>
	    <div class="nav-search">
		<form id="search" name="search" action="/search" method="GET" role="search" class="navbar-search">		  
			<input id="searchwords" placeholder="search..." class="search-query" name="searchwords" type="text">
		</form>
	    </div>
	    <div class="menu-items user-login">
			<ul>
			<li id="shownsfw"><a href="javascript:void(0)" onclick="toggleNSFW();" id="shownsfwlink">show NSFW</a></li>
			<li id="fblogin"><a href="javascript:void(0)" onclick="doLogin();" id="fbloginlink">login</a><a href="javascript:void(0)" id="fblogintext" style="display:none;"></a></li>
		</ul>
		</div>
	    <div class="clear"></div>
	</div>
</div>
	<!-- end top nav bar-->
	<!-- begin main content-->
<div id="container">
		<div class="page-content">
		<div class="post-wrap">

				<div id="posts">

	
</main>
<div id="header"></div> 

<div ng-controller="TaskController">

    <!-- // Modal -->
</div>

<!-- Jquery JS file -->
<script type="text/javascript" src="lib/jquery-3.3.1.min.js"></script>
<!-- AngularJS file -->
<script type="text/javascript" src="lib/angular-1.6.10/angular.min.js"></script>
<!-- Bootstrap JS file -->
<script type="text/javascript" src="bootstrap/js/bootstrap.min.js"></script>
<!-- Custom JS file -->
<script type="text/javascript" src="lib/app.js"></script>
</body>
</html>
