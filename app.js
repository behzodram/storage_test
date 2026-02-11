// config initialized with config.js content

firebase.initializeApp(firebaseConfig);
const storage = firebase.storage();


/* 📤 UPLOAD */
function uploadFile(){

    const file = document.getElementById("fileInput").files[0];
    if(!file) return alert("Fayl tanlanmadi");

    const ref = storage.ref("uploads/" + Date.now() + "_" + file.name);
    const task = ref.put(file);

    /* Progress */
    task.on("state_changed", snap => {

        const percent = (snap.bytesTransferred / snap.totalBytes) * 100;
        document.getElementById("progressBar").style.width = percent + "%";

    }, console.error, async () => {

        const url = await ref.getDownloadURL();

        document.getElementById("preview").innerHTML = `
            <p><b>Download URL:</b></p>
            <a href="${url}" target="_blank">${url}</a>
            <br>
            <img src="${url}">
        `;

        alert("Upload tugadi ✅");
    });
}


/* 📂 LIST FILES */
async function listFiles(){

    const listRef = storage.ref("uploads");
    const res = await listRef.listAll();

    const box = document.getElementById("fileList");
    box.innerHTML = "";

    for(const item of res.items){

        const url = await item.getDownloadURL();

        box.innerHTML += `
        <div class="file-box">
            <a href="${url}" target="_blank">${item.name}</a>
            <button onclick="deleteFile('${item.fullPath}')">
                Delete
            </button>
        </div>
        `;
    }
}


/* 🗑️ DELETE */
async function deleteFile(path){

    if(!confirm("O'chirilsinmi?")) return;

    await storage.ref(path).delete();

    alert("O'chirildi");
    listFiles();
}