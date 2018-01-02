var quill = new Quill('#editor-container', {
  modules: {
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
      ['image', 'code-block'],
      [{'color':[]},{'background':[]}]

    ]
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'  ,// or 'bubble'
  // readOnly:true
});