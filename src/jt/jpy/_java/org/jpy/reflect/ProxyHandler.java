//
//
//

package org.jpy.reflect;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.util.Arrays;

import org.jpy.PyObject;
import org.jpy.PyLib;

import static org.jpy.PyLib.assertPythonRuns;

public final class ProxyHandler implements InvocationHandler
{
    private       PyObject           target;
    private final PyLib.CallableKind callableKind;

    public ProxyHandler(PyObject target, PyLib.CallableKind callableKind)
    {
        if ( target == null )
            throw new NullPointerException("target");

        this.target       = target;
        this.callableKind = callableKind;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable
    {
        assertPythonRuns();

        if ( (PyLib.Diag.getFlags() & PyLib.Diag.F_METH) != 0 )
            System.out.printf("org.jpy.reflect.ProxyHandler: " +
                              "invoke: %s(%s) on target=%s in thread %s\n",
                              method.getName(), Arrays.toString(args),
                              Long.toHexString(this.target.getPointer()),
                              Thread.currentThread());

        return PyLib.callAndReturnValue(this.target.getPointer(),
                                        callableKind == PyLib.CallableKind.METHOD,
                                        method.getName(),
                                        (args != null) ? args.length : 0, args,
                                        method.getParameterTypes(),
                                        method.getReturnType());
    }

    @Override
    protected void finalize() throws Throwable
    {
        try
        {
            this.finalize(this.target.getPointer());
            this.target = null;
        }
        finally
        {
            super.finalize();
        }
    }

    private native void finalize(long target);
}
