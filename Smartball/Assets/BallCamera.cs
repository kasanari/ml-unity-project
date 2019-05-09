using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using MLAgents;

public class BallCamera : MonoBehaviour
{


    float rayDistance = 2f;
    float[] rayAngles = {45f, 90f, 135f, 180f, 225f, 270f, 315f};
    string[] detectableObjects = { "wall", "goal" };
    private RayPerception3D rayPer;


    Quaternion rotation;
    void Awake()
    {
        rayPer = GetComponent<RayPerception3D>();
        this.transform.position = this.transform.parent.transform.position + new Vector3(0, 1, 0);
        rotation = transform.rotation;
    }
    void LateUpdate()
    {
        this.transform.position = this.transform.parent.transform.position + new Vector3(0, 1, 0);
        transform.rotation = rotation;
    }

    public List<float> getObs()
    {
        return rayPer.Perceive(rayDistance, rayAngles, detectableObjects, 0f, 0f);
    }
}
