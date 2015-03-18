$ ->
  $('a[data-oauth]').each ->
    $(this).click ->
      $('#remember_me').val $(this).attr('data-oauth')
      $('#login_form').submit()
