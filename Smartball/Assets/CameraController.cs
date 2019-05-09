using UnityEngine;
using System.Collections;

public class CameraController : MonoBehaviour
{

    public GameObject player;

    private Vector3 offset;

    void Start()
    {
        offset = new Vector3(15f, 15f, 0);
    }

    void LateUpdate()
    {
        //transform.position = player.transform.position + offset;

    }

    public void ResetCamera()
    {
        //transform.position = player.transform.position + offset;
    }
    
}