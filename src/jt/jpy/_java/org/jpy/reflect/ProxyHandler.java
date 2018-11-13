// Copyright 2014-2018 Adam Karpierz
// Licensed under the Apache License, Version 2.0
// http://www.apache.org/licenses/LICENSE-2.0

package org.jpy.reflect;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;
import java.lang.reflect.Method;
import java.util.Arrays;

import org.jpy.PyObject;
import org.jpy.PyLib;

import static org.jpy.PyLib.assertPythonRuns;

public final class ProxyHandler implements InvocationHandler
{
    // Used by the proxy instances created by the PyObject.createProxy(Class)
    // and PyModule.createProxy(Class) methods.

    private final PyObject           pyObject;
    private final PyLib.CallableKind callableKind;

    public ProxyHandler(PyObject pyObject, PyLib.CallableKind callableKind)
    {
        if ( pyObject == null )
            throw new NullPointerException("pyObject");

        this.pyObject     = pyObject;
        this.callableKind = callableKind;
    }

    @Override
    public Object invoke(Object proxyObject, Method method, Object[] args) throws Throwable
    {
        assertPythonRuns();

        if ( (PyLib.Diag.getFlags() & PyLib.Diag.F_METH) != 0 )
            System.out.printf("org.jpy.reflect.ProxyHandler: invoke: %s(%s) on pyObject=%s in thread %s\n",
                              method.getName(), Arrays.toString(args), Long.toHexString(this.pyObject.getPointer()),
                              Thread.currentThread());

        String   methodName = method.getName();
        Class<?> returnType = method.getReturnType();

        if ( method.equals(hashCodeMethod) )
        {
            return this.callPythonHash();
        }

        if ( method.equals(equalsMethod) )
        {
            if ( ! this.isProxyEqualsEligible(proxyObject, args[0]) )
                return false;

            PyObject otherPyObject = this.proxyGetOtherPyObject(proxyObject, args[0]);
            if ( this.pyObject == otherPyObject )
                return true;

            args[0] = otherPyObject;
            if ( ! this.pyObject.hasAttribute("__eq__") )
                return false;

            PyObject eqMethPtr = this.pyObject.getAttribute("__eq__");
            if ( ! eqMethPtr.hasAttribute("__func__") )
                // Must not be implemented
                return false;

            // It's proxy eligible, but not same object,
            // and __eq__ was implemented so defer to the Python __eq__
            methodName = "__eq__";
        }
        else if ( method.equals(toStringMethod) )
        {
            methodName = "__str__";
        }

        return PyLib.callAndReturnValue(this.pyObject.getPointer(),
                                        this.callableKind == PyLib.CallableKind.METHOD,
                                        methodName,
                                        args != null ? args.length : 0, args,
                                        method.getParameterTypes(), returnType);
    }

    private boolean isProxyEqualsEligible(Object proxyObject, Object otherObject)
    {
        // Determines if the two proxy objects implement the same interfaces

        return (proxyObject.getClass() == otherObject.getClass() &&
                Arrays.deepEquals(proxyObject.getClass().getInterfaces(),
                                  otherObject.getClass().getInterfaces()));
    }

    private PyObject proxyGetOtherPyObject(Object proxyObject, Object otherObject)
    {
        // Determines the corresponding Python object for the other object passed

        InvocationHandler otherProxyHandler = Proxy.getInvocationHandler(otherObject);
        return (otherProxyHandler.getClass() == this.getClass())
               ? ((ProxyHandler) otherProxyHandler).pyObject : null;
    }

    private int callPythonHash()
    {
        // Calls the Python __hash__ function on the Python object, and returns the
        // last 32 bits of it, since Python hash codes are 64 bits on 64 bit machines.

        long pythonHash = PyLib.callAndReturnValue(this.pyObject.getPointer(),
                                                   true, "__hash__",
                                                   0, null,
                                                   new Class<?>[0], Long.class);
        return (int) pythonHash;
    }

    @Override
    protected void finalize() throws Throwable
    {
        try
        {
            this.release(this.pyObject.getPointer());
            //this.pyObject = null;
        }
        finally
        {
            super.finalize();
        }
    }

    // preloaded Method objects for the methods in java.lang.Object
    private static Method hashCodeMethod;
    private static Method equalsMethod;
    private static Method toStringMethod;

    static
    {
        try
        {
            hashCodeMethod = Object.class.getMethod("hashCode");
            equalsMethod   = Object.class.getMethod("equals", new Class[] { Object.class });
            toStringMethod = Object.class.getMethod("toString");
        }
        catch ( NoSuchMethodException exc )
        {
            throw new NoSuchMethodError(exc.getMessage());
        }
    }

    private native void initialize(long target);
    private native void release(long target);
}
