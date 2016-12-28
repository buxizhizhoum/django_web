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

            if (obj_temp.statues == 1){
                var temp = obj_temp.favor_count;
                $(point).children().eq(1).text(temp)
            }else{
                alert(obj_temp.message)
            }
        },
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
    var replies = $(point).prev().val();
    $(point).prev().val("");
    console.log("replies")
    console.log(replies)
    $.ajax({
        url:"/blog/submitreply/",
        type: "POST",
        data:{replies: replies, id: id},
        success: function (callback) {
            var temp_obj = jQuery.parseJSON(callback);
            var replies = temp_obj.replies;
            var username = temp_obj.username;
            console.log(temp_obj)
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
function sendchat(point){
    var content = $(point).parent().parent().prev().children().eq(0).children().eq(0).val();
    $(point).parent().parent().prev().children().eq(0).children().eq(0).val("");
    $.ajax({
        url: "/blog/sendchat/",
        type: "POST",
        data: {content: content},
        success: function (callback) {
            var data = jQuery.parseJSON(callback);
            var content = "<p style='color: blue'>" + data.user + "</p>" +
                "<p style='font-size: medium'>" + data.content + "</p>";
            $(point).parent().parent().prev().prev().children().eq(0).append(content)
        }

    })
}