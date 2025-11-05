echo ""


if ! pgrep -x "mongod" > /dev/null; then
    echo "mongodb is not running. starting mongodb..."
    brew services start mongodb/brew/mongodb-community 2>/dev/null || echo "Please start MongoDB manually"
    sleep 2
fi



python3 api.py &
BACKEND_PID=$!


sleep 3


cd frontend
npm run dev &
FRONTEND_PID=$!


echo "   Backend:  http://localhost:5000"
echo "   Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"


trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

