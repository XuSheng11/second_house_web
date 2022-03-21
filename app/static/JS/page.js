
//获取当前总页数
let currentPage = document.getElementById("currentPage");
let totalPage = document.getElementById("totalPage");

//获取页数
let totalNum = parseInt(document.getElementById("totalNum").innerText);
if (totalNum < 20){
    totalPage.value = "1";
}else{
    totalPage.value = ( Math.floor(totalNum / 20) + 1).toString();
}

//改变页面中的page值 （page,页数）
function replaceParamVal(url,paramName,replaceWith) {
    var oUrl = url;
    var re=eval('/('+ paramName+'=)([^&]*)/gi');
    var nUrl = oUrl.replace(re,paramName+'='+replaceWith);
    this.location = nUrl;
    window.location.href=nUrl;
}

//按钮跳转

//获取当前页面page值
    let curPage = 1
    let url = window.location.href;
    let pattern =/page=\d{1,}/ig

    let page = url.match(pattern)
    if (page===null){
        curPage = 1;
        if(url.includes('?')){
            url = url+"&page=1";
        }
        else{
            url = url+"?page=1"
        }
        console.log(curPage)
    }else{
        curPage = parseInt(page[0].split('=')[1]);
        console.log(curPage)
    }
    currentPage.value = curPage;


function page_option(pagename) {
    //跳转
    console.log(totalPage.value);
    switch (pagename) {
        //第一页
        case -1:
            curPage = 1;
            break;
        //最后一页
        case -2:
            curPage = parseInt(totalPage.value);
            break;
        //上一页
        case -3:
            if (curPage > 1) {
                curPage = curPage - 1;
            } else {
                curPage = 1;
            }
            break;
        //下一页
        case -4:
            if (curPage < parseInt(totalPage.value)) {
                curPage = curPage + 1;
            } else {
                curPage = parseInt(totalPage.value);
            }
            break;
        default:
            curPage = 1;
            break;
    }

    //跳转
    replaceParamVal(url,'page',curPage);
    // window.location.href = "list.html?curPage=" + curPage;
    currentPage.value = curPage;
}

//输入跳转
function page_turn(){
    let aimPage = parseInt(currentPage.value);
    if (!(aimPage>=1 && aimPage <= parseInt(totalPage.value))){
        aimPage = 1;
    }
    console.log(aimPage)
    replaceParamVal(url,'page',aimPage);
    // window.location.href = "list.html?curPage=" + aimPage;
    currentPage.value = aimPage;

}