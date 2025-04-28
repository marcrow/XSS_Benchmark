<!-- scenario_01.yaml -->
id: 1
name: "Scenario 1 - <p> block"
description: "Injection into a <p> tag"
category: "HTML Injection"
template_block: "p_block"
html_snippet: |
  <p>{{ payload }}</p>
js_snippet: |
  // No custom JS

---
<!-- scenario_02.yaml -->
id: 2
name: "Scenario 2 - img onmouseover"
description: "Injection into an image's onmouseover attribute"
category: "Attribute Injection"
template_block: "img_onmouseover_block"
html_snippet: |
  <img src="#" onmouseover="{{ payload }}">
js_snippet: |
  // No custom JS

---
<!-- scenario_03.yaml -->
id: 3
name: "Scenario 3 - script inline"
description: "Injection into an inline script"
category: "Script Injection"
template_block: "script_inline_block"
html_snippet: |
  <script>
  {{ payload }}
  </script>
js_snippet: |
  // No custom JS

---
<!-- scenario_04.yaml -->
id: 4
name: "Scenario 4 - input hidden"
description: "Injection into a hidden input value"
category: "Form Injection"
template_block: "input_hidden_block"
html_snippet: |
  <input type="hidden" name="data" value="{{ payload }}">
js_snippet: |
  // No custom JS

---
<!-- scenario_05.yaml -->
id: 5
name: "Scenario 5 - img src"
description: "Injection into an image src attribute"
category: "Attribute Injection"
template_block: "img_src_block"
html_snippet: |
  <img src="{{ payload }}">
js_snippet: |
  // No custom JS

---
<!-- scenario_06.yaml -->
id: 6
name: "Scenario 6 - a href"
description: "Injection into an anchor href attribute"
category: "Attribute Injection"
template_block: "a_href_block"
html_snippet: |
  <a href="{{ payload }}">Click here</a>
js_snippet: |
  // No custom JS

---
<!-- scenario_07.yaml -->
id: 7
name: "Scenario 7 - script src"
description: "Injection into a script src attribute"
category: "Script Injection"
template_block: "script_src_block"
html_snippet: |
  <script src="{{ payload }}"></script>
js_snippet: |
  // No custom JS

---
<!-- scenario_08.yaml -->
id: 8
name: "Scenario 8 - button onclick"
description: "Injection into a button's onclick attribute"
category: "Attribute Injection"
template_block: "button_onclick_block"
html_snippet: |
  <button onclick="{{ payload }}">Click me</button>
js_snippet: |
  // No custom JS

---
<!-- scenario_09.yaml -->
id: 9
name: "Scenario 9 - textarea"
description: "Injection into a textarea value"
category: "Form Injection"
template_block: "textarea_block"
html_snippet: |
  <textarea>{{ payload }}</textarea>
js_snippet: |
  // No custom JS

---
<!-- scenario_10.yaml -->
id: 10
name: "Scenario 10 - comment"
description: "Injection into an HTML comment"
category: "HTML Injection"
template_block: "comment_block"
html_snippet: |
  <!-- {{ payload }} -->
js_snippet: |
  // No custom JS

---
<!-- scenario_11.yaml -->
id: 11
name: "Scenario 11 - script JSON"
description: "Injection into a JSON object in a script"
category: "Script Injection"
template_block: "script_json_block"
html_snippet: |
  <script>
  var obj = {"callback": "{{ payload }}"};
  </script>
js_snippet: |
  // No custom JS

---
<!-- scenario_12.yaml -->
id: 12
name: "Scenario 12 - select option"
description: "Injection into a select option value"
category: "Form Injection"
template_block: "select_option_block"
html_snippet: |
  <select><option value="{{ payload }}">Payload</option></select>
js_snippet: |
  // No custom JS

---
<!-- scenario_13.yaml -->
id: 13
name: "Scenario 13 - div style"
description: "Injection into a div style attribute"
category: "Attribute Injection"
template_block: "div_style_block"
html_snippet: |
  <div style="{{ payload }}">Styled</div>
js_snippet: |
  // No custom JS

---
<!-- scenario_14.yaml -->
id: 14
name: "Scenario 14 - meta refresh"
description: "Injection into a meta refresh URL"
category: "HTML Injection"
template_block: "meta_refresh_block"
html_snippet: |
  <meta http-equiv="refresh" content="1;url={{ payload }}">
js_snippet: |
  // No custom JS

---
<!-- scenario_15.yaml -->
id: 15
name: "Scenario 15 - title"
description: "Injection into a page title"
category: "HTML Injection"
template_block: "title_block"
html_snippet: |
  <title>{{ payload }}</title>
js_snippet: |
  // No custom JS

---
<!-- scenario_16.yaml -->
id: 16
name: "Scenario 16 - script var"
description: "Injection into a JS variable in a script"
category: "Script Injection"
template_block: "script_var_block"
html_snippet: |
  <script>
  var msg = "{{ payload }}";
  </script>
js_snippet: |
  // No custom JS

---
<!-- scenario_17.yaml -->
id: 17
name: "Scenario 17 - div data attribute"
description: "Injection into a div data-info attribute"
category: "Attribute Injection"
template_block: "div_data_block"
html_snippet: |
  <div data-info="{{ payload }}">Element</div>
js_snippet: |
  // No custom JS

---
<!-- scenario_18.yaml -->
id: 18
name: "Scenario 18 - table cell"
description: "Injection into a table cell"
category: "HTML Injection"
template_block: "table_block"
html_snippet: |
  <table><tr><td>{{ payload }}</td></tr></table>
js_snippet: |
  // No custom JS

---
<!-- scenario_19.yaml -->
id: 19
name: "Scenario 19 - input placeholder"
description: "Injection into an input placeholder"
category: "Form Injection"
template_block: "input_placeholder_block"
html_snippet: |
  <input placeholder="{{ payload }}">
js_snippet: |
  // No custom JS

---
<!-- scenario_20.yaml -->
id: 20
name: "Scenario 20 - iframe src"
description: "Injection into an iframe src attribute"
category: "HTML Injection"
template_block: "iframe_block"
html_snippet: |
  <iframe src="{{ payload }}"></iframe>
js_snippet: |
  // No custom JS