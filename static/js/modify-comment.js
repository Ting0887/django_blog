function buttonClick(idx) {
  b = document.getElementsByClassName("dropdown-content")[idx].classList.toggle("show");
}

function editComment(usercomment, idx){
  document.getElementById("comment-"+idx).innerHTML = 
  '<input type="text" name="comment" value='+usercomment+'></input>';
  document.getElementById("confirm-edit-"+idx).innerHTML = '<input class="btn" type="submit" value="確認">';

  document.getElementById("cancel-edit-"+idx).innerHTML = 
  '<a href="">取消</a>';
  document.querySelectorAll(".comment-dropdown").forEach(e => e.remove());
}
