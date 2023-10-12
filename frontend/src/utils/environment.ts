interface Environment {
    apiUrl: string,
    prod: boolean,
}

const environmentDev: Environment = {
    apiUrl: 'http://localhost:8000',
    prod: false
}

const environmentProd: Environment = {
    apiUrl: '',
    prod: true
}

let environment: Environment;

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
if (window.location.host.includes('localhost')) {
    environment = environmentDev
} else {
    environment = environmentProd
}

export default environment;