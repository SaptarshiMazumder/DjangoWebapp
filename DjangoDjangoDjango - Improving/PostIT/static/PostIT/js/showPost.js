function expandPost(json, this_) {
    post_id = json['post_id'];
    body = json['body'];
    image_data = json['image_data'];
    author = json['author'];
    total_likes = json['total_likes'];
    liked = json['liked'];
    // replies_to_post = json['replies_to_post'];
    parents_arr = json['parents_arr'];
    last_viewed = json['last_viewed'];
    has_images = json['has_images']
    has_video = json['has_video']
    post_images_url = json['post_images_url']
    post_video_url = json['post_video_url']
    like_count = json['like_count']
    serialized_replies = json['serialized_replies']

    console.log("post_id " + post_id)
    console.log("Body " + body)
    console.log("image_data " + image_data)
    console.log("Author " + author)
    console.log("Total likes " + total_likes)
    console.log("liked " + liked)
    // console.log("replies_to_post " + replies_to_post)
    console.log("parents_arr " + parents_arr)
    console.log("last_viewed " + last_viewed)
    console.log("has_images " + has_images)
    console.log("has_images " + typeof has_images)
    console.log("has_video " + has_video)
    console.log("post_images_url " + post_images_url)
    console.log("post_video_url " + post_video_url)
    console.log("like_count " + like_count)
    console.log('serialized_replies ' + serialized_replies)
    console.log("THIS: ", this_)



    document.getElementById("post-body").innerHTML = body
    if (has_images === true) {
        var img = document.createElement("img");
        img.src = post_images_url[0]
        img.setAttribute("height", "300px");
        var className = "post-img";
        img.setAttribute("class", className)
        img.setAttribute("id", "post-img")
        var src = document.getElementById("post-body-images");

        src.appendChild(img);

        var br = document.createElement("br")
        src.appendChild(br)

        var i = 1;
        post_images_url.forEach((imgUrl) => {
            var radio = document.createElement("input")
            radio.setAttribute("type", "radio")
            radio.setAttribute("name", "img")
            var radioId = "img" + i.toString()
            radio.setAttribute("id", radioId)
            radio.setAttribute("value", imgUrl)
            radio.addEventListener("change", findSelected)
            if (i === 1) {
                radio.checked = true;
            }

            var src = document.getElementById("post-body-images");
            src.appendChild(radio)


            i += 1;

        })
        i = 1;

    }

    if (has_video === true) {
        console.log("THIS POST HAS VIDEO")
        var video = document.createElement("video")
        video.src = post_video_url
        video.autoplay = false;
        video.controls = true;
        video.muted = false;
        video.height = 240; // 👈️ in px
        video.width = 320; // 👈️ in px
        var src = document.getElementById("post-body-video")
        src.appendChild(video)

    }

    popupContainer.classList.add('show');


    var postInteractElement = document.getElementById("post-interact")
    var likeBtn = document.createElement("button")
    likeBtn.setAttribute("id", "like-button")
    likeBtn.setAttribute("class", "like-button")
    likeBtn.setAttribute("name", like_count)
    likeBtn.setAttribute("value", post_id)
    likeBtn.innerHTML = "LIKED BY " + like_count.toString()
    //postInteractElement.appendChild(likeBtn)


    var replyBtn = document.createElement("a")
    var link = "/post/reply/" + post_id.toString()
    replyBtn.setAttribute('href', link)
    replyBtn.innerHTML = "Reply"



    postInteractElement.appendChild(likeBtn)
    postInteractElement.appendChild(replyBtn)


    var postRepliesElement = document.getElementById("post-replies")
    serialized_replies.forEach((replyObj) => {
        console.log(replyObj)

        var replyAuthor = document.createElement("div")
        var replyBody = document.createElement("a")
        var replyLink = "/post/" + replyObj['post_id']
        replyBody.setAttribute('href', replyLink)
        var br = document.createElement("br")
        replyBody.innerHTML = replyObj['body']
        replyAuthor.innerHTML = "@" + replyObj['author']

        var replyImagesDiv = document.createElement("div")
        var replyVideoDiv = document.createElement("div")
        if (replyObj['has_images'] === true) {
            replyImagesUrl = replyObj['reply_images_url']
            replyImagesUrl.forEach(imgUrl => {
                var img = document.createElement("img");
                img.src = imgUrl;
                img.setAttribute("height", "300px");
                var className = "reply-img";
                img.setAttribute("class", className)
                img.setAttribute("id", "reply-img")
                replyImagesDiv.appendChild(img)
            });
        }

        if (replyObj['has_video'] === true) {
            console.log("THIS POST HAS VIDEO")
            var video = document.createElement("video")
            video.src = replyObj['reply_video_url']
            video.autoplay = false;
            video.controls = true;
            video.muted = false;
            video.height = 240; // 👈️ in px
            video.width = 320; // 👈️ in px

            replyVideoDiv.appendChild(video)

        }

        replyBody.appendChild(replyImagesDiv)
        replyBody.appendChild(replyVideoDiv)

        var interactReplyDiv = document.createElement("div")
        var likeReplyBtn = document.createElement("button")
        likeReplyBtn.setAttribute("id", "like-button")
        likeReplyBtn.setAttribute("class", "like-button")
        likeReplyBtn.setAttribute("name", replyObj['like_count'])
        likeReplyBtn.setAttribute("value", replyObj['post_id'])
        likeReplyBtn.innerHTML = "LIKED BY " + replyObj['like_count'].toString()


        var replyTypesDiv = document.createElement("div")
        replyTypesDiv.setAttribute("class", "dropdown")

        var replyTypesButton = document.createElement("button")
        replyTypesButton.setAttribute("class", "btn btn-secondary dropdown-toggle")
        replyTypesButton.setAttribute("id", "dropdownMenuButton1")
        replyTypesButton.setAttribute("type", "button")
        replyTypesButton.setAttribute("data-bs-toggle", "dropdown")
        replyTypesButton.setAttribute("aria-expanded", "false")
        replyTypesButton.innerHTML = "reply"

        replyTypesList = document.createElement("ul")
        replyTypesList.setAttribute("class", "dropdown-menu")
        replyTypesList.setAttribute("aria-labelledby", "dropdownMenuButton1")

        replyTypeTextList = document.createElement("li")
        replyTypeTextLink = document.createElement("a")
        replyTypeTextLink.innerHTML = "Text"
        replyTypeTextList.appendChild(replyTypeTextLink)

        replyTypeImageList = document.createElement("li")
        replyTypeImageLink = document.createElement("a")
        replyTypeImageLink.innerHTML = "Image"
        replyTypeImageList.appendChild(replyTypeImageLink)

        replyTypeVideoList = document.createElement("li")
        replyTypeVideoLink = document.createElement("a")
        replyTypeVideoLink.innerHTML = "Image"
        replyTypeVideoList.appendChild(replyTypeVideoLink)

        replyTypesList.appendChild(replyTypeTextList)
        replyTypesList.appendChild(replyTypeImageList)
        replyTypesList.appendChild(replyTypeVideoList)

        replyTypesDiv.appendChild(replyTypesButton)
        replyTypesDiv.appendChild(replyTypesList)



        var replyReplyBtn = document.createElement("a")
        var linkReply = "/post/reply/" + replyObj['post_id'].toString()
        replyReplyBtn.setAttribute('href', linkReply)
        replyReplyBtn.innerHTML = "Reply"

        interactReplyDiv.appendChild(likeReplyBtn)
        interactReplyDiv.appendChild(replyReplyBtn)
        interactReplyDiv.appendChild(replyTypesDiv)


        postRepliesElement.appendChild(replyAuthor)
        postRepliesElement.appendChild(br)
        postRepliesElement.appendChild(replyBody)
        postRepliesElement.appendChild(br)
        postRepliesElement.appendChild(interactReplyDiv)
        postRepliesElement.appendChild(br)

    })





}