function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Like & Unlike Post (Toggle)
function likePost(postId) {
    fetch(`/post/${postId}/like/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const likeCount = document.getElementById(`like-count-${postId}`);
                const likeIcon = document.getElementById(`like-icon-${postId}`)

                likeCount.textContent = data.likes_count;
                likeIcon.classList.toggle("fa-thumbs-up");
                likeIcon.classList.toggle("fa-thumbs-o-up");
                likeIcon.classList.toggle("text-blue-500", data.liked);
            } else {
                console.error(`Error : ${data.message}`);
            }
            // location.reload();
        })
        .catch(error => {
            console.error(`Error: ${error}`); location.reload();
        });
}

// Follow * Unfollow User
function followUnfollow(userId) {
    fetch(`/profile/${userId}/follow/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        credentials: "same-origin",
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const followBtn = document.getElementById(`follow-btn-${userId}`);
                const followersCount = document.getElementById(`followers-count-${userId}`);

                followBtn.textContent = data.is_following ? "Unfollow" : "Follow";
                followersCount.textContent = `Followers: ${data.followersCount}`;
            } else {
                console.error(`Error: ${error.message}`);
            }
        })
        .catch(error => {
            console.error(`Error: ${error}`);
            location.reload();
        });
}


// Delete Post
function deletePost(postId) {
    if (!confirm("Are you sure you want to delete this post?")) {
        return;
    }

    fetch(`/post/${postId}/delete/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json",
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = "/";
        } else {
            alert("Error: " + data.error);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    })
}


