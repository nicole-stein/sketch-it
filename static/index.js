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

  $("#button-to-main-page").click(() => {
    console.log("changing")
    change_to("#main-page")
  })

  $(".info-box-link").click(function () {
    select_image($(this).data("n"))
  })

  images = []
  $('.info-box-image').each(function () {
    images.push(this.src)
  })

  function select_image(n) {

    $(".drawing_image").delay( 150 ).fadeOut( 600 )
    img = document.createElement("img")
    $(img).attr("class", "drawing_image")
    $(img).attr("src", images[n - 1])
    $(img).css("display", "none")
    document.querySelector("#drawing_image_col").appendChild(img)
    $(img).delay(300).fadeIn(200)
    $("#poof_gif").fadeIn(200).delay(1000).fadeOut(200)
  }



})
