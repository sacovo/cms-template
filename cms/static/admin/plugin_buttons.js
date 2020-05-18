/* global ContentEditor, django */
(function($) {
  $(document).on('content-editor:ready', function() {
    var buttons = [
      ['_header', '<i class="fa fa-heading"></i>'],
      ['_button', '<i class="fa fa-square"></i>'],
      ['_divider', '<i class="fa fa-horizontal-rule"></i>'],
      ['_richtext', '<i class="fa fa-pencil"></i>'],
      ['_image', '<i class="fa fa-image"></i>'],
      ['_external', '<i class="fa fa-film"></i>'],
      ['_html', '<i class="fa fa-code"></i>'],
      ['_formplugin', '<i class="fa fa-poll"></i>'],

      ['_gallery', '<i class="fa fa-images"></i>'],
      ['_slide', '<i class="fa fa-image"></i>'],
      ['_snippet', '<i class="fa fa-cog"></i>'],
      ['_table', '<i class="fa fa-table"></i>'],
      ['_team', '<i class="fa fa-users"></i>'],
      ['_person', '<i class="fa fa-user"></i>'],
      ['_eventplugin', '<i class="fa fa-calendar"></i>'],
      ['_articleplugin', '<i class="fa fa-archive"></i>'],
      
    ]

    for (var i = 0; i < buttons.length; ++i) {
      ContentEditor.addPluginButton('cms' + buttons[i][0], buttons[i][1])
      ContentEditor.addPluginButton('blog' + buttons[i][0], buttons[i][1])
      ContentEditor.addPluginButton('events' + buttons[i][0], buttons[i][1])
    }
  })
})(django.jQuery)
