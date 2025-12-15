import { useEffect, useState } from 'react';
import axios from "axios";
function ArticleList() {
    const [articles, setArticles] = useState([]);
    axios.get('/api/hello').then((res) => {
        console.log(res.data.message)
    })
    useEffect(() => {

        fetch('/api/articles')
            .then(res => res.json())
            .then(data => setArticles(data));
    }, []);

    return (
        <div>
            <h2>Articles culturels</h2>
            {articles.map(a => (
                <div key={a.id}>
                    <h3>{a.titre}</h3>
                    <p>{a.contenu}</p>
                </div>
            ))}
        </div>
    );
}

export default ArticleList;