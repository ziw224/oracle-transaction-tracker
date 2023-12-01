export default (state, action) => {
    switch (action.type) {
        case 'ADD_TRANSACTION':
            return {
                ...state,
                transactions: [action.payload, ...state.transactions]
            };
        case 'SET_INITIAL_STATE':
            return {
                ...state,
                transactions: action.payload
            };
        case 'SET_USER_COUNT':
            return {
                ...state,
                userCount: action.payload
            };
        default:
            return state;
    }
};
