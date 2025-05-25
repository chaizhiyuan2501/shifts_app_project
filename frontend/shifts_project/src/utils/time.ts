export const getTime = () => {
    let message = "";
    let hours = new Date().getHours();
    if (hours <= 9) {
        message = "おはおう"
    } else if (hours <= 18) {
        message = "こんにちは"
    } else {
        message = "こんばんは"
    }
    return message;
}