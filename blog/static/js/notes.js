/**
 * Created by hasee on 2016/12/16.
 */
// javascript functions complete the below tasks:
// 1. send data to a certain url
// 2. wait and get the data from the functions used to deal with data
// 3. process those data, put them on the web pages or sth else.

function ChangeTab(point) {
            $(point).siblings().removeClass("active");
            $(point).addClass("active");
        }
function add_favor(point, id){
    $.ajax({
        url: "/blog/addfavor/",
        type: "POST",
        data: {id: id},
        success: function (callback) {
            var obj_temp = jQuery.parseJSON(callback);
            // 如果statues值=1，表明后台点赞成功，在前台更新点赞数，否则显示错误信息
            if (obj_temp.statues == 1){
                var temp = obj_temp.favor_count; // 获取后台信息
                $(point).children().eq(1).text(temp); // 更新
            }else{
                alert(obj_temp.message)
            }
        },
        // 如果ajax发送数据没成功，执行这个。
        error: function () {
            console.log("add favor failed")
        }
    })
}
function get_reply(point, id) {
    $.ajax({
        url: "/blog/getreply/",
        type: "POST",
        data:{id: id},
        success: function (callback) {
            var obj_temp = jQuery.parseJSON(callback);
            var replies = obj_temp.replies; //replies contains a dictionary
            var reply_count = obj_temp.reply_count;
            $(point).children().eq(1).text(reply_count);
            $(point).parent().parent().parent().next().children().children().eq(0).val("");
            // 对获取到的replies字典执行循环，做字符串拼接
            $.each(replies, function (k,v) {
                $(point).parent().parent().parent().next().children().children().eq(0).prepend(
                    "<p style='color: #999'>" + v.user__username + "</p>" +
                    "<p>" + v.content + "</p>");
            });
            $(point).parent().parent().parent().next().children().children().eq(0).parent().toggleClass("hide")
        }
    })
}
function submit_reply(point, id){
    var replies = $(point).prev().val();  //获取输入框中的值
    $(point).prev().val("");  //clear
    console.log("replies");
    console.log(replies);
    $.ajax({
        url:"/blog/submitreply/",
        type: "POST",
        data:{replies: replies, id: id},
        success: function (callback) {
            var temp_obj = jQuery.parseJSON(callback);
            var replies = temp_obj.replies;
            var username = temp_obj.username;
            // 如果后台在数据库添加成功，则在前端显示提交的回复。
            console.log(temp_obj);
            if (temp_obj.statues == 1){
                $(point).parent().prev().append("<p style='color: #999'>" + username + "</p>" +
                "<p>" + replies + "</p>");
            }
        }
    })
}
function add_notes(point){
    $.ajax({
        url: "/blog/addnotes/",
        type: "POST",
        data: {}
    })
}

window.content_chat = new Array();// {} is ok.
// dict definiation has to be out of function, otherwise when function run
// at every click, the dictionary will be created again with content cleared.
function active_tag(point){
    // 1. username_to original
    // 2. store info in username_to dict
    // 3. refresh username_to info
    // 4. get info from dict with new username_to
    console.log('click');
    var username_to = $(".list-group-item.active").children().eq(1).text();//get info before change statues of list
    window.content_chat[username_to] = $("#chatting_box").html();//store info
    $("#chatting_box").html('');//clear
    console.log('before click');
    console.log(username_to);
    console.log(window.content_chat[username_to]);
    $(point).addClass("active");
    $(point).siblings().removeClass("active");
    var contact_id = $(point).attr("contact_id");
    var contact_type = $(point).attr("contact_type");
    var username_to = $(point).children().eq(1).text();//refresh username_to
    var username_from = $(point).attr("username_from");
    console.log('after click');
    console.log(username_to);
    console.log(window.content_chat[username_to]);
    $("#chatting_box").html(window.content_chat[username_to]);// get info of new username_to
    console.log(username_from, username_to, contact_id, contact_type);
    $("#title").text("Chatting with " + username_to);
    // after click change the message count and hide badge.
    var filter_str = "[username_badge = " + username_to + "]";  //属性选择
    $(".badge").filter(filter_str).addClass("hide");
    $(".badge").filter(filter_str).text('0');
}
function get_new_messages(username_from, username_to){
            console.log('get new message');
            console.log(username_from, username_to);
            $.ajax({
                url: '/blog/getnewmessages/',
                data: {"username_from":username_from, "username_to":username_to},
                type: "POST",
                success: function (callback) {
                    var data = jQuery.parseJSON(callback);
                    console.log('data in get new message');
                    console.log(data);
                    $.each(data, function(k,v){
                        var content = "<p style='color: blue'>" + v.user + ":" +
                        "<span style='color:black'>" + v.time + "</span>" + "</p>" +
                        "<p style='font-size:medium'>" + v.content + "</p>";
                        // judge if the messages is not belong to current active window user. do not append
                        // to it.
                        console.log('v.user');
                        console.log(v.user);
                        console.log($(".list-group-item.active").children().eq(1).text())
                        if (v.user == $(".list-group-item.active").children().eq(1).text()){
                            // if the message comes from is belong to the active user.
                            $("#chatting_box").append(content);
                        }
                        else{
                            // if the message not belong to the active user, save it to dict.
                            console.log('not chatting one')
                            if (window.content_chat[v.user]){
                                // if there is content in dict, append
                                // else add
                                window.content_chat[v.user] += content
                            }else{
                                window.content_chat[v.user] = content
                            }
                            // new message count
                            // get value, add 1, set.
                            var filter_str = "[username_badge = " + v.user + "]";
                            var message_count_on_web = parseInt($(".badge").filter(filter_str).text());
                            console.log(message_count_on_web);
                            message_count_on_web += 1;
                            $(".badge").filter(filter_str).text(message_count_on_web);
                            $(".badge").filter(filter_str).removeClass("hide")
                        }
                    });
                    var height = document.getElementById('chatting_box').scrollHeight;
                    $('#chatting_box').scrollTop(height);
                    return get_new_messages(username_from,username_to)
                }

            });
            //get_new_messages(username_from,username_to)
        }
function sendchat(point){
    //var content = $(point).parent().prev().text(); // 获取到输入框的内容
    var content = $("#textarea").text();
    console.log("---------------");
    console.log(content);
    var username_to = $(".list-group-item.active").children().eq(1).text();
    // there is no space between two class, means that choose the element that has two classes.
    console.log('username_to at send chat in js');
    console.log(username_to);
    var username_from = $(point).attr("username_from");
    get_new_messages(username_from, username_to);
    //$(point).parent().prev().html("");  // 清空输入框内容
    $("#textarea").text("");
    $.ajax({
        url: "/blog/sendchat/",
        type: "POST",
        data: {content: content, 'username_to' :username_to, 'username_from': username_from},
        success: function (callback) {
            console.log(callback);
            var data = jQuery.parseJSON(callback);
            console.log('data in send');
            console.log(data);
            $.each(data, function(k,v){
                var content = "<p style='color: blue'>" + v.user + ":" +
                "<span style='color:black'>" + v.time + "</span>" + "</p>" +
                "<p style='font-size:medium'>" + v.content + "</p>";
                //$(point).parent().prev().prev().prev().prev().append(content)
                $("#chatting_box").append(content)
            });
            var height = document.getElementById('chatting_box').scrollHeight;
            $('#chatting_box').scrollTop(height)
        }
    })
}
function upload(point){
    var form_data = new FormData();
    var chatting_file = $("#chatting_file")[0].files[0];
    console.log(chatting_file);
    form_data.append("file",$("#chatting_file")[0].files[0]);
    $.ajax({
        url: "/blog/uploadfile/",
        data: form_data,
        type: "POST",
        processData: false,  //不做数据处理
        contentType: false,  //不发送contentType.
        success: function(callback){
            console.log(callback);
            var image_url = "<img src="+ "http://127.0.0.1:8000/" + callback+ "/>";
            //$("#for_image").removeClass(hide);
            $("#textarea").html(image_url);
            //$("#for_image").html(image_url);
            //$("#textarea").html($(image_url).html());
            // 这个地方能在输入框显示图片吗？
        }
    });
    //upload_progress($("#chatting_file")[0].files[0])
}

// function upload_progress(file_obj) {
//     // 把文件名发送给后端，让其通过文件名查询文件传输大小，回传至后端，改变滚动条
//     var filename = file_obj.name;
//     $.ajax({
//         url: "/blog/chat/upload_progress",
//         data: {filename: filename},
//         type: "get",
//         success: function (callback) {
//             console.log('file size');
//             console.log(callback)
//         }
//     })
// }