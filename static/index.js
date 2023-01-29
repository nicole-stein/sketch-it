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

  
  // Animate the entrance of the board
  $(".drawing_image").css('opacity', "0")
  $("#drawing_image_wrapper").width($(".drawing_image").width())
  setTimeout(()=>{

    $("#drawing_image_wrapper").addClass('animate__animated animate__zoomIn')
  }, 100)
  setTimeout(()=>{
    s  = document.querySelector("#drawing_sound")
    
    console.log("SOUND")
    $("#poof_gif").fadeIn(200).delay(1000).fadeOut(200)
  }, 500)
  setTimeout(()=>{
    $(".drawing_image").animate({ opacity: 1 }, 700)
  }, 1200)
  



  images = []
  $('.info-box-image').each(function (index) {
    images.push(this.src)
    setTimeout(
      () => {
        $(this).css("display", "block")
        $(this).addClass('animate__animated animate__flipInX')
    },
    1800 + 70 * index
    )
  })

  function select_image(n) {
    $("#drawing_image_wrapper").removeClass()
    setTimeout(
      () => {
        $("#drawing_image_wrapper").attr('class', 'animate__animated animate__wobble')
        
      },
      350
    )
    $(".drawing_image").delay( 300 ).fadeOut( 600 )
    $("#drawing_sound")[0].play()
    img = document.createElement("img")
    $(img).attr("class", "drawing_image")
    $(img).attr("src", images[n - 1])
    $(img).css("display", "none")
    document.querySelector("#drawing_image_wrapper").appendChild(img)
    $(img).delay(750).fadeIn(200)
    $("#poof_gif").fadeIn(200).delay(1000).fadeOut(200)
  }



})
