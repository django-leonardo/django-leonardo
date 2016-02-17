/**
 * Add JS resource to DOM, if not exists
 * @example loadJsResource({src:'/my.js',async:true,defer:true}) or loadJsResource("/my.js") or arrays of them 
 * loadJsResource(["/lol.js","/lol2.js",{src:"/lol2",async:true}])
 * USE ONLY ABSOLUTE PATHS
 */
function loadResource(scripts){
    var addScriptFn = function(script){
        var scripts = document.getElementsByTagName('script'),found=false;
        for(var i=0;i<scripts.length;i++){
            var fullSrc = (script.src.indexOf("://") > -1)?script.src:window.location.protocol+"//"+script.src;
            if(scripts[i].src===fullSrc){
                found=true;
                break;
            }
        }
        if(!found){
            var domScript = document.createElement('script'); 
            domScript.type = "text/javascript";
            domScript.src = script.src;
            domScript.async = script.async && script.async==true;
            domScript.defer = script.defer && script.defer==true;
            scripts[0].parentNode.insertBefore(domScript, scripts[0]);
        }
    };
    if(scripts instanceof Array){
        for(var i=0;i<scripts.length;i++){
            if(typeof scripts[i] === 'object' && scripts[i].hasOwnProperty("src")){
                addScriptFn(scripts[i]);
            }else if(typeof scripts[i] === 'string'){
                addScriptFn({src:scripts[i]});
            }else{
                console.log("JS Resource #"+i+" is invalid!");
            }
        }
    }else{
        if(typeof scripts === 'object' && scripts.hasOwnProperty("src")){
            addScriptFn(scripts);
        }else if(typeof scripts === 'string'){
            addScriptFn({src:scripts});
        }else{
            console.log("JS Resource is invalid!");
        }
    }
}