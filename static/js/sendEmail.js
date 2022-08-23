function showmessage() {
        var msg = document.forms["form"]["email"].value;
        if(msg == null || msg == ""){
            alert("請輸入使用者信箱")
        }
        else{
            alert('已經發送重設密碼資訊到您的信箱，如果沒收到，請確認您的信箱是否輸入錯誤')
        }
        return false;
}
