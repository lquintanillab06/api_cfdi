let openScript;

let results = document.getElementById("results")
let form = document.querySelector('form');
let editor = document.getElementById("editor");
let buttonSave = document.getElementById("button-save")
let buttonOpen = document.getElementById("button-open")
let buttonClear = document.getElementById("button-clear")
let buttonClean = document.getElementById("button-clean")

document.addEventListener("DOMContentLoaded",(event)=>{
      if(openScript){
        results.innerHTML = ""
      }
})

editor.addEventListener("keydown", function(event) {
  if (event.key === "Tab") {
    event.preventDefault(); 
    let start = this.selectionStart;
    console.log("Start",start)
    let end = this.selectionEnd;
    console.log("End",end)
    this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
    console.log("Value",this.value)
    this.selectionStart = this.selectionEnd = start + 1;
    console.log("SS",this,this.selectionStart)
  }
});



buttonSave.addEventListener("click",(e)=>{
  console.log("Salvando Script")
  Swal.fire({
    title: 'Script Name',
    input: 'text',
    inputAttributes: {
      autocapitalize: 'off'
    },
    showCancelButton: true,
    confirmButtonText: 'Save',
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      const name = `${result.value}`
      const content = editor.value;
      console.log("Name",name)
      const blob = new Blob([content], { type: 'text/plain' });
      const anchor = document.createElement('a');
      anchor.download = `${name}.txt`;
      anchor.href = URL.createObjectURL(blob);
      anchor.click();

    }
  })
}) 


buttonOpen.addEventListener("click",(e)=>{
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = '.txt'; 
  input.onchange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      editor.value = content;
      openScript = fileName;
    };
    reader.readAsText(file);
  };
  input.click();
})



form.addEventListener('submit', function() {
    results.innerText = "";
    let loader = document.getElementById('loader');
    loader.style.display = 'block';  
});

buttonClear.addEventListener('click', function() {
  results.innerText = "";
  });

buttonClean.addEventListener('click', function() {
  Swal.fire({
    title: 'Clean Editor?',
    showCancelButton: true,
    confirmButtonText: 'Accept',
    allowOutsideClick: () => !Swal.isLoading()
  }).then((result) => {
    if (result.isConfirmed) {
      editor.value = "";
    }
  })
  }); 



