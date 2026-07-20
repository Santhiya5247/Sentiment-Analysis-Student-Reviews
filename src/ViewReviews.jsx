import { useEffect, useState } from "react";
import API from "./api";

function ViewReviews() {

    const [reviews, setReviews] = useState([]);

    useEffect(() => {
        fetchReviews();
    }, []);

    const fetchReviews = async () => {

        try {

            const response = await API.get("/reviews");

            setReviews(response.data);

        } catch (error) {

            console.log(error);

            alert("Unable to fetch reviews");

        }

    };

    return (

        <div style={{padding:"30px"}}>

            <h2 style={{textAlign:"center"}}>All Student Reviews</h2>

            <table
                border="1"
                cellPadding="10"
                style={{
                    width:"100%",
                    borderCollapse:"collapse",
                    marginTop:"20px"
                }}
            >

                <thead>

                    <tr>

                        <th>Student</th>
                        <th>Course</th>
                        <th>Trainer</th>
                        <th>Review</th>
                        <th>Sentiment</th>
                        <th>Date</th>

                    </tr>

                </thead>

                <tbody>

                    {
                        reviews.map((item)=>(
                            <tr key={item.id}>

                                <td>{item.student_name}</td>
                                <td>{item.course_name}</td>
                                <td>{item.trainer_name}</td>
                                <td>{item.review}</td>
                                <td>{item.sentiment}</td>
                                <td>{item.review_date}</td>

                            </tr>
                        ))
                    }

                </tbody>

            </table>

        </div>

    );

}

export default ViewReviews;