$(document).ready ->

  set_tooltips()
  fix_cover_imgs()
  $(window).resize -> fix_cover_height()

set_tooltips = ->
  $('.tooltipster').each ->
    content = $('span', $(this)).html()
    $(this).tooltipster { content: content, position: 'bottom', theme: 'tooltipster-findaconf' }

fix_cover_imgs = ->
  $('img.cover').each ->
    img_url = $(this).attr 'src'
    console.log img_url
    parent = $(this).parent()
    css_value = "url('" + img_url + "')"
    parent.css 'background-image', css_value
    parent.html '&nbsp;'
    fix_cover_height parent.parent()
    $(this).hide()

fix_cover_height = (row=false) ->
  if !row
    row = $('div.result')
  row.each ->
    cover = $('div', $(this)).first()
    main = $('div.small-8', $(this)).first()
    height = main.height()
    cover.css 'height', height + 'px'