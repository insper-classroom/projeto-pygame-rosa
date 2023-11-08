async function getCommits() {
    let user = "insper-classroom";
    let repo = "projeto-pygame-rosa";
    const token = "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";
        
    let url = `https://api.github.com/repos/${user}/${repo}/commits?per_page=100`;

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/vnd.github+json",
                "Authorization": `Bearer ${token}`,
                "X-GitHub-Api-Version": "2022-11-28"
            }
        });

        const data = await response.json();

        let container = document.querySelector("#commits");
        container.style.textAlign = "center";
        container.style.color = "white";

        for (let i in data) {
            container.innerHTML += `
                <p>${data[i].commit.author.name} - ${data[i].commit.message} / ${data[i].commit.author.date}</p>
            `;
        }
    } catch (error) {
        // Trate erros aqui, se houver algum
        console.error("Erro ao fazer a requisição:", error);
    }
}

getCommits();
