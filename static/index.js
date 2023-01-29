document.addEventListener("DOMContentLoaded", () => {
  function change_to(div) {
    if ($(div).css("display") == "none") {
      let all_children = document.querySelector("#root").children
      for (let i = 0; i < all_children.length; i++) {
        $(all_children[i]).fadeOut()
      }
      setTimeout(() => {
        $(div).fadeIn()
      }, 400)
    }
  }

  $("#button-to-main-page").click(()=>{
    console.log("changing")
    change_to("#main-page")
  })

  $("#change_button").click(()=>{
    console.log("changing...")
    document.getElementById("drawing_sound").play();
    $("#changing_gif").fadeIn( 200 ).delay( 1000 ).fadeOut( 200 )


  })




})
