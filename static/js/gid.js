!function(a,b){h={player:function(a,d){b.getElementById("pleer-video").innerHTML="";var e=b.createElement("iframe");if(e.src=a,e.width="100%",e.height="100%",e.allow="autoplay *; fullscreen *", e.setAttribute("border","0"),e.setAttribute("frameborder","0"),e.setAttribute("scrolling","no"),e.setAttribute("allowfullscreen","true"),b.getElementById("pleer-video").appendChild(e),b.getElementById("serii-club")){c=b.getElementById("serii-club").getElementsByTagName("span");for(var f=0;f<c.length;f++)c[f].removeAttribute("class")}d.setAttribute("class","active")},season:function(a,d){if(b.getElementById("pleer-zvuk")){c=b.getElementById("pleer-zvuk").getElementsByTagName("span");for(var e=0;e<c.length;e++)b.getElementById("season"+e).style.display="none",c[e].removeAttribute("class");b.getElementById("season"+a).style.display="";var g=b.getElementById("season"+a).getElementsByTagName("span")[0];g.click(),f=a}d.setAttribute("class","active")},show:function(a,c){
b.write('<div id="pleer-gid" align="center"><ul id="pleer-zvuk"><li id="seasons"></li></ul><div id="pleer-video"></div><div class="serii-s"><ul id="serii-club"></ul></div><div class="playlists-prev1"></div><div class="playlists-next1"></div></div>');

for(var d=0;d<a.length;d++)b.getElementById("pleer-zvuk")
	.getElementsByTagName("li")[0].innerHTML+='<span onclick="uvk.season('+d+', this)">'+a[d]+"</span>",
b.getElementById("serii-club").innerHTML+='<div class="sea'+d+'"><li id="season'+d+'" style="display:none;"></li></div>';

for (var d = 0; d < a.length; d++) {
	for (var e = 0; e < c[d].length; e++) {
        if (a[d] == 'Автоперевод') var serii = "<span id='autos' onclick=\"uvk.player('//" + decodeURIComponent(c[d][e]) + "', this);\">Выбор серий в плеере</span>";
		else  var serii = "<span onclick=\"uvk.player('//" + decodeURIComponent(c[d][e]) + "', this);\"> "+(e+1)+" <em>серия</em></span>";
b.getElementById("season"+d).innerHTML+=
 ''+ serii + '';
}}

b.getElementById("pleer-zvuk").getElementsByTagName("span")[0].setAttribute("class","active"),b.getElementById("pleer-zvuk").getElementsByTagName("span")[0].click(),b.getElementById("season0").getElementsByTagName("span")[0].click(),b.getElementById("season0").style.display=""},

},"undefined"!=a.uvk&&(a.uvk=h)}(window,document);
var pos=0,poz=0,sea=null,vk=new Object;vk={init:function(){document.write('<div id="treyler-club" align="center">\t \t                  <ul id="treyler-seri"></ul> \t \t                   <div id="treyler-player"></div>\t \t                <ul id="treyler-season"><li id="seasonis"></li></ul>   \t \t                   \t                       \t                       <a href="javascript://" class="prev1" onclick="vk.move1(1);">prev</a>\t                       <a href="javascript://" class="next1" onclick="vk.move1(0);">next</a>\t                       </div>')},player:function(e,t){document.getElementById("treyler-player").innerHTML="";var n=document.createElement("iframe");if(n.src=String(e),n.width="100%",n.height="305",n.setAttribute("border","0"),n.setAttribute("frameborder","0"),n.setAttribute("scrolling","no"),n.setAttribute("allowfullscreen",""),n.setAttribute("webkitallowfullscreen",""),n.setAttribute("mozallowfullscreen",""),n.setAttribute("oallowfullscreen",""),n.setAttribute("msallowfullscreen",""),document.getElementById("treyler-player").appendChild(n),document.getElementById("treyler-seri")){c=document.getElementById("treyler-seri").getElementsByTagName("span");for(var l=0;l<c.length;l++)c[l].removeAttribute("class")}t.setAttribute("class","active")},seasoni:function(e,t){if(document.getElementById("treyler-season")){c=document.getElementById("treyler-season").getElementsByTagName("span");for(var n=0;n<c.length;n++)document.getElementById("seasoni"+n).style.display="none",c[n].removeAttribute("class");document.getElementById("seasoni"+e).style.display="",sea=e}t.setAttribute("class","active")},showi:function(e,t){for(n=0;n<e;n++)document.getElementById("treyler-season").getElementsByTagName("li")[0].innerHTML+='<span onclick="vk.seasoni('+n+', this)">Сезон '+(n+1)+"</span>",document.getElementById("treyler-seri").innerHTML+='<li id="seasoni'+n+'" style="display:none;"></li>';for(var n=0;n<e;n++)for(var l=0;l<t[n].length;l++)document.getElementById("seasoni"+n).innerHTML+="<span onclick=\"vk.player('"+t[n][l]+"', this);\">Видео "+(l+1)+"</span>";document.getElementById("treyler-season").getElementsByTagName("span")[0].setAttribute("class","active"),document.getElementById("treyler-season").getElementsByTagName("span")[0].click(),document.getElementById("seasoni0").getElementsByTagName("span")[0].click(),document.getElementById("seasoni0").style.display=""},move:function(e){var t,n=document.getElementById("seasonis"),l=n.offsetWidth,s=n.offsetLeft;0==e&&(clearTimeout(void 0),t=setInterval(function(){(pos-=10)>=s-width&&pos>=-(l-width)?n.style.left=pos+"px":clearTimeout(t)},15)),1==e&&(clearTimeout(t),t=setInterval(function(){(pos+=10)<=s+width&&pos<=0?n.style.left=pos+"px":clearTimeout(t)},15))},move1:function(e){var t,n=document.getElementById("seasoni"+sea),l=n.offsetWidth,s=n.offsetLeft;0==e&&(clearTimeout(void 0),t=setInterval(function(){(poz-=10)>=s-width&&poz>=-(l-width)?n.style.left=poz+"px":clearTimeout(t)},15)),1==e&&(clearTimeout(t),t=setInterval(function(){(poz+=10)<=s+width&&poz<=0?n.style.left=poz+"px":clearTimeout(t)},15))}};
