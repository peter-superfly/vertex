import "../styles/App.scss";
import Head from "next/head";
import {ThemeProvider} from 'next-themes'

function MainApp({Component, pageProps}) {
    return (<ThemeProvider  defaultTheme="system">
        <Head>
            <title>Vertex</title>
            <link rel="icon" type="image/x-icon" href="favicon.svg"/>
        </Head>
        <Component {...pageProps}/>
    </ThemeProvider>);
}


export default MainApp;
