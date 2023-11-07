export default (state, action) => {
    switch(action.type) {
        case 'ADD_TRANSACTION':
            return {
                ...state, // initial state
                // action.payload will add the new transaction to the inital array of transactions 
                transactions: [action.payload, ...state.transactions]
            }
        default:
            return state;
    }
}